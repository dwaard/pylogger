import threading, datetime

class ProcessingThread(threading.Thread):

  def __init__(self, source, writer):
    threading.Thread.__init__(self)
    self.setDaemon(True)
    self.source = source
    self.writer = writer


  def start(self):
    threading.Thread.start(self)


  def run(self):
    for item in self.source:
      self.writer.write(item)

