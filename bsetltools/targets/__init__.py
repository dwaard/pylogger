import logging
from bsetltools.targets.PlotTarget import PlotTarget
from bsetltools.targets.FileTarget import FileTarget


def plotTarget(*args, **kwargs):
  """
  A target that uses Matplotlib to plot the data as a lineplot.
  """
  return PlotTarget(*args, **kwargs)


def consoleTarget(*args, **kwargs):
  """
  A target that prints the data to the console.
  """
  class ConsoleTarget:
    def __init__(self, *args, serializer=None, verbosity=0, **kwargs):
      self.verbosity = verbosity
      self.serializer = serializer

    def write(self, item):
      if self.serializer is not None:
        item = self.serializer.serialize(item.copy())
      print(item)

  return ConsoleTarget(*args, **kwargs)


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
  return FileTarget(*args, **kwargs)


def multiTarget(targets):
  """
  A target that writes the data to the specified list of other targets.
  """
  class MultiTarget:
    def write(self, item):
      for target in targets:
        target.write(item)
  return MultiTarget()
