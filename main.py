import os
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import bsetltools
from bsetltools import ( sources, transformers, targets )
from bsetltools.ProcessingThread import ProcessingThread
import logging
import csv
from bsetltools.configparser import ConfigMap
import warnings

import yaml

def buildLogFilename():
  filename = os.getenv('FILELOGGERFILENAME')
  if filename is None:
    raise Exception('FILELOGGERFILENAME is not set')

  if os.getenv('FILELOGGERWILLADDTIMESTAMP', False).lower() in ["true", "1", "yes"]:
      # Create the timestamp
      format = os.getenv('FILELOGGERTIMESTAMPFORMAT', "%d-%m-%Y_%H_%M_%S")
      timestamp = datetime.now().strftime(format)
      # Use Path to breakup the filename
      path = Path(filename)
      filename = path.with_name(f"{path.stem}_{timestamp}{path.suffix}")
  return filename


def main():
  args = bsetltools.init()
  # Load YAML
  with open('config.yaml', 'r') as f:
    raw_config = yaml.safe_load(f)

  # Validate and parse with Pydantic
  # TODO verwijder model_dump, zodat alle variabelen makkelijker uitleesbaar zijn
  # dit heeft wel veel impact op de rest van de code
  config = ConfigMap(**raw_config).model_dump()
  # config = raw_config

  # source = sources.random_generator(list(config.values()), delimiter=';', wait_time=0.25)
  # source = sources.file('.out/log.csv', mode='r', newline='', encoding='utf-8')
  source = sources.serial(port='COM3', baudrate=115200, encoding='utf-8')

  source = transformers.csv(source, delimiter = ";")
  source = transformers.timestampExtender(source, format=config['timestamp']['params']['format'])
  # source = transformers.rowDictTransformer(source, list(config.keys()))
  source = transformers.parser(source, config, args.verbose)

  fig, axes = plt.subplots()
  plt.title('Proofingcontroller')

  writemode = os.getenv('FILELOGGERWRITEMODE', 'x')
  target = targets.multiTarget([
    targets.plotTarget(axes, config),
    targets.consoleTarget(),
    targets.fileTarget(buildLogFilename(), writemode)
  ])
  # excelreader = sources.excel('.out/log.xlsx')

  thread = ProcessingThread(source, target)
  thread.start()
  with warnings.catch_warnings(action="ignore"):
    plt.legend()
  plt.show()


if __name__ == '__main__':
  main()