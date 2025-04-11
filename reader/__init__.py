import os
from reader.serialreader import SerialReader
from reader.csvreader import CSVReader
from reader.randomreader import RandomReader


def build():
  type = os.getenv('READERTYPE')
  match type:
    case "serial":
      return SerialReader()
    case "csv":
      return CSVReader()
    case "random":
      return RandomReader()
    case _:
      raise Exception("Onbekend READERTYPE=%s. Controleer je .env of --readertype parameter." % type)
