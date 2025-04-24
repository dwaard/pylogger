import threading
import logging

class ProcessingThread(threading.Thread):
  """
  A thread that processes items from a source and writes them using a writer.
  
  Attributes:
    source (iterable): The input source yielding items to be processed.
    writer (object): An object with a write(item) method to handle output.
  """

  def __init__(self, source, writer):
    """
    Initializes the ProcessingThread with a source and a writer.
    
    Args:
      source (iterable): An iterable data source to consume.
      writer (object): An object that implements a write(item) method.
    """
    threading.Thread.__init__(self)
    self.setDaemon(True)
    self.source = source
    self.writer = writer
    logging.debug("ProcessingThread initialized")

  def start(self):
    """
    Starts the thread by invoking the start method of the parent class.
    """
    threading.Thread.start(self)
    logging.debug("ProcessingThread started")

  def run(self):
    """
    Iterates over the source and writes each item using the writer.
    
    This method is called automatically when the thread starts.
    """
    for item in self.source:
      logging.debug(f"ProcessingThread writing '{item}'")
      self.writer.write(item)
