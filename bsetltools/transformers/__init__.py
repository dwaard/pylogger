import datetime
from bsetltools.transformers.Parser import Parser
from collections.abc import Iterable


def rowDictTransformer(source, keys):
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
  for line in source:
    yield dict(zip(keys, line))


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


def timestampExtender(source, format=None, timestamp_key='timestamp', timestamp_column=0):
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
  for item in source:
    value = datetime.datetime.now()
    if format is not None:
        value = value.strftime(format)
    if isinstance(item, dict):
      if timestamp_key not in item:
        item[timestamp_key] = value
    elif isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
      if len(item) > timestamp_column and not isinstance(item[timestamp_column], datetime.datetime):
        item.insert(timestamp_column, value)
    yield item