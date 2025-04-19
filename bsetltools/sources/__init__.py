import csv as csv_module
from bsetltools.sources.OpenpyxlSource import OpenpyxlSource
import serial as serial_module
import rstr
import time  # Voor de wachttijd
import random


def file(*args, **kwargs):
  """
  Opens a file. It is basically a convenient wrapper that calls the `open()` function.

  See for the available arguments: https://docs.python.org/3/library/functions.html#open
  """
  return open(*args, **kwargs)



def csv(*args, **kwargs):
  """
  Opens a CSV file. It is basically a convenient wrapper that calls the `csv.reader()` function.

  See for the available arguments: https://docs.python.org/3/library/csv.html#csv.reader
  """
  return csv_module.reader(*args, **kwargs)


def excel(*args, **kwargs):
  """
  Opens an Excel file using Openpyxl. 
  """
  return OpenpyxlSource(*args, **kwargs)


def serial(*args, encoding=None, **kwargs):
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
  com = serial_module.Serial(*args, **kwargs)
  if not com.is_open:
    com.open()
  com.reset_input_buffer()
  if encoding is None:
    return com
  for line in com:
    if not line:
      break
    yield line.decode(encoding).strip()



def random_generator(configs, delimiter=',', wait_time=0):
  """
  Generates CSV-style strings based on a list of config dictionaries.
  Each dictionary must contain 'type' ('regex' or 'number'), 'min', and 'max', and
  may optionally include 'decimals' for number types or 'pattern' for regex types.

  Parameters:
    configs (list of dict): Each dict can contain:
      - 'type' (str): Either 'regex' or 'number'.
      - 'min' (float): Lower bound for 'number' type.
      - 'max' (float): Upper bound for 'number' type.
      - 'decimals' (int, optional): Number of decimal places for 'number' type (default: 2).
      - 'pattern' (str, optional): Regex pattern for 'regex' type.
    delimiter (str): The delimiter to separate values in the output string (default: ',').

  Returns:
    list: List of random values based on the config.
  """
  while True:
    results = []

    for cfg in configs:
      type = cfg['type']
      params = cfg['params']
      if type == 'int':
        min_val = params['min']
        max_val = params['max']
        value = int(round(random.uniform(min_val, max_val), 0))
        results.append(str(value))
      elif type == 'float':
        min_val = params['min']
        max_val = params['max']
        decimals = params.get('decimals', -1)
        value = random.uniform(min_val, max_val)
        if decimals >= 0:
          value = round(value, decimals)
        results.append(f"{value:.{decimals}f}")      
      elif cfg['type'] == 'regex':
        pattern = params.get('pattern')
        if pattern:
          value = rstr.xeger(pattern)  # Gebruik rstr om een string op basis van regex te genereren
          results.append(value)
        else:
          raise ValueError("Pattern must be specified for 'regex' type.")
      
      else:
        raise ValueError("Invalid type in config. Must be 'regex' or 'number'.")

      # Voeg wachttijd toe als deze groter is dan 0
      if wait_time > 0:
        time.sleep(wait_time)

    yield delimiter.join(results)  


def socket(*args, **kwargs):
  """
  Opens a socket for reading. 

  NOTE: The socket opens in binary mode, so iterating it yields byte streams. You can use the ByteLineTransformer
        to solve this.

  TODO: Implement this when needed
  """
  raise NotImplementedError("If you need this, you need to implement this")

