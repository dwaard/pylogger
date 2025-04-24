import matplotlib.pyplot as plt
import bsetltools
from bsetltools import ( sources, transformers, targets )
from bsetltools.ProcessingThread import ProcessingThread
import warnings, logging


config = {
  "timestamp" : {
    "parser" : { "type" : "datetime", "required" : True, "format" : "%Y-%m-%d %H:%M:%S.%f" },
    "plotter" : {
      "axis" : {
        "location" : "x",
        "format": "%H:%M:%S"
      },
    }
  },
  "set" : {
    "parser" : { "type" : "float", "required" : True, "min": -50, "max": 50, "decimals": 2 },
    "plotter" : {
      "axis" : {
        "location" : "right", 
        "title" : "Temp (°C)",
        "limits" : { "auto" : True, "links" : ["set", "measured"] }
      },
      "line" : { "color" : "red" },
      "label" : { "template" : "Set: {value:.1f}°C", "color" : "red"},
    }
  },
  "measured" : {
    "parser" : { "type" : "float", "required" : True, "min": -50, "max": 50, "decimals": 2 },
    "plotter" : {
      "axis" : { "location" : "none" },
      "line" : { "color" : "blue" },
      "label" : { "template" : "In: {value:.1f}°C"},
    }
  },
  "duty_cycle" : {
    "parser" : { "type" : "float", "required" : True, "min": 0, "max": 5, "decimals": 2 },
    "plotter" : {
      "axis" : {
        "location" : "left",
        "title" : "Out (sec)",
        "limits" : { "ymin" : 0, "ymax" : 5 },
      },
      "line" : { "color" : "green" },
      "label" : { "template" : "Out: {value:.2f}sec"},
    }
  },
}


delimiter = ';'
timestamp_parser_format = config['timestamp']['parser']['format']
parser_rules = {k: v["parser"] for k, v in config.items()}
random_rules = {k: v for k, v in parser_rules.items() if k != "timestamp"}
plotter_configs = {k: v["plotter"] for k, v in config.items()}


def remove_output_column(row):
  if len(row) >= 5:
    return row[:3] + row[4:5]
  return row


def buildSource(args):
  stream = None
  # Here, choose either random or serial as a source. both streams require the timestamp prepended
  # so, uncomment that line also
  # stream = sources.random(random_rules, delimiter=delimiter, verbosity=args.verbose)
  stream = sources.serial(port='COM3', baudrate=115200, encoding='utf-8', verbosity=args.verbose)
  if stream:
    stream = transformers.timestampExtender(stream, format=timestamp_parser_format, verbosity=args.verbose)
  # the different file streams already have a timestamp
  # stream = sources.file('.out/log_20-04-2025_13_40_59.csv', mode='r', newline='', encoding='utf-8', verbosity=args.verbose)
  # stream = sources.multifile('.out', pattern='log_*.csv', verbosity=args.verbose)
  # split as csv and parse using the config rules
  stream = transformers.csv(stream, delimiter=delimiter, verbosity=args.verbose)
  stream = transformers.mapper(stream, remove_output_column, args.verbose)
  stream = transformers.parser(stream, parser_rules, verbosity=args.verbose)
  # stream = transformers.paced_iter(stream, 0.25, args.verbose)
  return stream


def buildTarget(args):
  serializer = transformers.serializer(None, parser_rules, delimiter=delimiter, verbosity=args.verbose)
  target = targets.multiTarget([
    targets.plotTarget(plotter_configs, title='Proofingcontroller', max_samples=1500),
    targets.consoleTarget(serializer=serializer),
    targets.fileTarget(bsetltools.buildTargetFilename('.out/log.csv'), 'w', serializer=serializer)
  ])
  return target
  # return targets.consoleTarget()


def main():
  args = bsetltools.init()
  stream = buildSource(args)
  target = buildTarget(args)

  # Simple, when no plotting is needed:
  # count = 0
  # for packet in stream:
  #   count += 1
  #   target.write(packet)
  # logging.info(f"Processed {count} rows")

  # Complex, when plotting is required (needs an extra Thread)
  thread = ProcessingThread(stream, target)
  thread.start()
  plt.show()


if __name__ == '__main__':
  main()