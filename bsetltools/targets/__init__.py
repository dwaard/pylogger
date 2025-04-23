import logging
from bsetltools.targets.PlotTarget import PlotTarget


def plotTarget(axes, config):
  """
  A target that uses Matplotlib to plot the data as a lineplot.
  """
  return PlotTarget(axes, config)


def consoleTarget():
  """
  A target that prints the data to the console.
  """
  class ConsoleTarget:
    def write(self, item):
      print(item)
  return ConsoleTarget()


def logTarget(level=logging.INFO):
  """
  A target that logs the data to the logging at the specified level.
  """
  class LoggingTarget:
    def write(self, item):
      logging.log(level, item)
  return LoggingTarget()


def fileTarget(*args, **kwargs):
  """
  A target that writes the data to the specified file.
  """
  f = open(*args, **kwargs)
  class FileTarget:
    def write(self, item):
      f.write(str(item))
      f.write('\n')
      f.flush()
  return FileTarget()


def multiTarget(targets):
  """
  A target that writes the data to the specified list of other targets.
  """
  class MultiTarget:
    def write(self, item):
      for target in targets:
        target.write(item)
  return MultiTarget()
