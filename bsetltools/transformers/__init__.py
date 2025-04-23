import csv as csv_module
import datetime
from bsetltools.transformers.Parser import Parser
from collections.abc import Iterable
import time  # Voor de wachttijd in de delayer
import logging


def mapper(source, callback_function, verbosity=0):
  if verbosity > 1:
    logging.info(f"MapperTransformer: opening {source}")
  for line in source:
    result = callback_function(line)
    if verbosity > 2:
      logging.debug(f"MapperTransformer: mapped {result}")
    yield result

def rowDictTransformer(source, keys, verbosity=0):
  """
  Convert an iterable of row values into dictionaries using provided keys.

  Parameters:
    source (iterable): A sequence of iterables (e.g., list of lists or tuples),
                       where each inner iterable represents a row of values.
    keys (list): A list of strings representing the dictionary keys.

  Yields:
    dict: A dictionary mapping each key to the corresponding value in the row.

  Example:
    >>> list(rows_to_dicts([[1, 'Alice'], [2, 'Bob']], ['id', 'name']))
    [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
  """
  if verbosity > 1:
    logging.info(f"RowDictTransformer: opening {source}{keys}")

  for line in source:
    result = dict(zip(keys, line))
    if verbosity > 2:
      logging.debug(f"RowDictTransformer: zipped {result}")
    yield result


def csv(*args, verbosity=0, **kwargs):
  """
  Convert input to tabular data according the CSV format. It is basically a convenient 
  wrapper that opens a `csv.reader()` function and yields all rows.

  See for the available arguments: https://docs.python.org/3/library/csv.html#csv.reader
  """
  if verbosity > 1:
    logging.info(f"CsvTransformer: opening {list(args)}{kwargs}")

  for row in csv_module.reader(*args, **kwargs):
    if verbosity > 2:
      logging.debug(f"CsvTransformer: converted {row}")
    yield(row)



def parser(source, rules=[], verbosity=0):
  """
  Converts an iterable of dicts containing strings as values into dicts where each
  value is parsed into a configured type and validated according configured parameters.

  Parameters:
    source (iterable): A sequence of iterables (e.g., list of lists or tuples),
                       where each inner iterable represents a row of dicts containing 
                       strings as values.
    rules (dict): A dict representing the expected keys, value types and validation parameters

  Yields
    dict: A dictionary TODO
  """
  return Parser(source, rules, verbosity)


def timestampExtender(source, format=None, timestamp_key='timestamp', timestamp_column=0, delimiter=';', verbosity=0):
  """
  Adds a timestamp to each item in the input iterable if it's missing.

  Parameters:
    source (iterable): A sequence of dicts or iterables (e.g., lists) to process.
    format (str, optional): If provided, the timestamp will be formatted as a string using this format.
    timestamp_key (str): Key to use when adding the timestamp to dicts. Default is 'timestamp'.
    timestamp_column (int): Index to insert the timestamp into for list-like iterables. Default is 0.

  Yields:
    Each item from the source, possibly extended with a current timestamp.
  """
  if verbosity > 1:
    kwargs = {
      'format' : format,
      'timestamp_key': timestamp_key,
      'timestamp_column' : timestamp_column,
      'delimiter' : delimiter,
      'verbosity' : verbosity,
    }
    logging.info(f"TimestampExtender: opening {source}{kwargs}")

  for item in source:
    value = datetime.datetime.now()
    if format is not None:
        value = value.strftime(format)
    if isinstance(item, str):
      item = f"{value}{delimiter}{item}"
    if isinstance(item, dict):
      if timestamp_key not in item:
        item[timestamp_key] = value
    elif isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
      if len(item) > timestamp_column and not isinstance(item[timestamp_column], datetime.datetime):
        item.insert(timestamp_column, value)
    yield item


def paced_iter(source, interval=0, verbosity=0):
  """
  Yield items from a source iterable with optional fixed time intervals.

  This generator yields each item from the given `source`. If `interval` is
  greater than 0, it enforces a delay between yields to maintain a consistent pace,
  using high-precision timing.

  Args:
    source: An iterable of items to yield.
    interval: Optional delay (in seconds) between yields. Default is 0 (no delay).

  Yields:
    Items from the source iterable, one by one, optionally spaced by `interval` seconds.
  """
  if verbosity > 1:
    kwargs = {
      'interval' : interval,
      'verbosity': verbosity,
    }
    logging.info(f"PacedItertransformer: starting {source}{kwargs}")
  next_time = time.perf_counter()
  for item in source:
    yield item
    # Voeg wachttijd toe als deze groter is dan 0
    if interval > 0:
      next_time += interval
      sleep_duration = max(0, next_time - time.perf_counter())
      if verbosity > 2:
        logging.debug(f"PacedItertransformer: sleeping for {sleep_duration}")
      time.sleep(sleep_duration)
      