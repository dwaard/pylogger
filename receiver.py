import threading, datetime

class Receiver(threading.Thread):

  def __init__(self, reader, parser, logger, plotter):
    threading.Thread.__init__(self)
    self.setDaemon(True)
    self.reader = reader
    self.parser = parser
    self.logger = logger
    self.plotter = plotter


  def start(self):
    threading.Thread.start(self)


  def run(self):
    for line in self.reader.read():
      valid, data = self.parser.parse(line)
      if (valid == True):
        self.logger.log(line)
        self.plotter.plot(data)
      else:
        print("Line '%s' is not valid." % line)

