import os
from logger.filelogger import FileLogger


class NoneLogger:

    def log(self, data):
        pass


class ConsoleLogger:

    def log(self, data):
        print(data)
  

def build():
  type = os.getenv('LOGGERTYPE')
  match type:
    case "none":
      return NoneLogger()
    case "console":
      return ConsoleLogger()
    case "csv":
      return FileLogger()
    case _:
      raise Exception("Onbekend LOGGERTYPE=%s. Controleer je .env of --loggertype parameter." % type)
