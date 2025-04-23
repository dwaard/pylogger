from bsetltools.sources.OpenpyxlSource import OpenpyxlSource
from bsetltools.sources.MultiFileSource import MultiFileSource
from bsetltools.sources.RandomSource import RandomSource
import serial as serial_module
import logging

def file(*args, verbosity=0, **kwargs):
  """
  Opens a file. It is basically a convenient wrapper that calls the `open()` function.

  See for the available arguments: https://docs.python.org/3/library/functions.html#open
  """
  if verbosity > 0:
    logging.info(f"FilesSource: opening {list(args)}{kwargs}")
  # Open the file in read mode
  with open(*args, **kwargs) as file:
    # Read each line in the file
    for line in file:
      line = line.strip()
      if verbosity > 1:
        logging.debug(f"FilesSource: read '{line}'")
      # Yield each line
      yield line


def serial(*args, encoding=None, verbosity=0, **kwargs):
  """
  Opens a serial port. It is basically a convenient wrapper that calls the `serial.Serial()` function.
  It also opens the port if needed and flushes the input buffer. 
  
  However when encoding is set, it will also encode the bytestream to a string using the provided encoding.

  NOTE: The port opens in binary mode, so iterating it yields byte streams. You can use the ByteLineTransformer
        to solve this.

  Parameters:
      encoding (str): The character encoding to use for decoding bytes.
                      Defaults to 'utf-8'.
      All other parameters are passed to the serial port
                      
  See for the available arguments: https://pyserial.readthedocs.io/en/latest/pyserial_api.html
  """
  if verbosity > 0:
    logging.info(f"SerialSource: creating com {args}")
  com = serial_module.Serial(*args, **kwargs)
  if not com.is_open:
    if verbosity > 1:
      logging.debug("SerialSource: opening port")
    com.open()
  elif verbosity > 1:
      logging.debug("SerialSource: port was already open")
  com.reset_input_buffer()
  for line in com:
    if not line:
      break
    if encoding is not None:
      line = line.decode(encoding).strip()
    if verbosity > 2:
      logging.debug(f"SerialSource: received '{line}'")
    yield line


def multifile(*args, **kwargs):
  """
  Opens a multi file source. 
  """
  return MultiFileSource(*args, **kwargs)


def excel(*args, **kwargs):
  """
  Opens an Excel file using Openpyxl. 
  """
  return OpenpyxlSource(*args, **kwargs)


def random(*args, **kwargs):
  """
  Opens a Random source. 
  """
  return RandomSource(*args, **kwargs)


def socket(*args, **kwargs):
  """
  Opens a socket for reading. 

  NOTE: The socket opens in binary mode, so iterating it yields byte streams. You can use the ByteLineTransformer
        to solve this.

  TODO: Implement this when needed
  """
  raise NotImplementedError("If you need this, you need to implement this")


def faker(*args, **kwargs):
  """
  Opens a Faker generator. 

  See: https://pypi.org/project/Faker/

  TODO: Implement this when needed
  """
  raise NotImplementedError("If you need this, you need to implement this")

