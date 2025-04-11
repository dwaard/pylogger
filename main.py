import argparse
from dotenv import load_dotenv
import os
import reader, parser, logger
import matplotlib.pyplot as plt
from receiver import Receiver
from plotter import Plotter

load_dotenv()

def parse_arguments():
  parser = argparse.ArgumentParser(description="Verwerk command line parameters.")
  
  # Voeg argumenten toe
  parser.add_argument("-t", "--readertype", type=str, required=False, help="Het type reader (serial, csv of random)")
  parser.add_argument("-l", "--loggertype", type=str, required=False, help="Het type logger (none, console, csv)")
  parser.add_argument("-p", "--serialport", type=str, required=False, help="De naam van de seriele poort, bijv. COM1")
  parser.add_argument("-b", "--serialbaudrate", type=str, required=False, help="De naam van de seriele poort, bijv. COM1")
  parser.add_argument("-f", "--csvreaderfilename", type=str, required=False, help="De naam van het csv bestand dat gebruikt wordt als reader")

  # Parse de argumenten
  args = parser.parse_args()

  for key, value in vars(args).items():
    if value is not None:
      env_key = key.upper()
      os.environ[env_key] = str(value)
      print(f"ENV gezet: {env_key}={value}")

  return args



def main():
  args = parse_arguments()  
  # setup the plot
  fig, axes = plt.subplots()
  r = Receiver(
    reader.build(), 
    parser.build(),
    logger.build(), Plotter(axes))
  r.start()
  plt.legend()
  plt.show()



if __name__ == '__main__':
  main()
