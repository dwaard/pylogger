import logging
from bsetltools.targets.PlotTarget import PlotTarget

def plotTarget(axes, config):
  return PlotTarget(axes, config)

def consoleTarget():
  class ConsoleTarget:
    def write(self, item):
      print(item)
  return ConsoleTarget()


def logTarget(level=logging.INFO):
  class LoggingTarget:
    def write(self, item):
      logging.log(level, item)
  return LoggingTarget()


def fileTarget(*args, **kwargs):
  f = open(*args, **kwargs)
  class FileTarget:
    def write(self, item):
      f.write(str(item))
      f.write('\n')
  return FileTarget()


def multiTarget(targets):
  class MultiTarget:
    def write(self, item):
      for target in targets:
        target.write(item)
  return MultiTarget()
