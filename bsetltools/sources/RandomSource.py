import logging
import rstr
import random

class RandomSource:
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

  def __init__(self, rules, delimiter=',', verbosity=0):
    if verbosity > 0:
      kwargs = {
        'delimiter' : delimiter,
        'verbosity': verbosity,
      }
      logging.info(f"RandomSource: starting {rules}{kwargs}")
    self.rules = rules
    self.delimiter = delimiter
    self.verbosity = verbosity


  def __iter__(self):
    return self


  def __next__(self):
    results = []
    for key, rule in self.rules.items():
      results.append(self.generate_field(key, rule))
    result = self.delimiter.join(results)
    if self.verbosity > 1:
      logging.debug(f"RandomSource: generated '{result}'")
    return result



  def generate_field(self, key, rule):
    if 'type' not in rule:
      raise ValueError(f"Rule for {key} vas no type")
    func_name = 'generate_' + rule['type']
    # find a generator method to call and call it
    method = getattr(self, func_name)
    return method(key, rule)


  def generate_int(self, rule):
    if 'min' in rule:
      min_val = rule['min']
    else:
      min_val = -2**31        # -2147483648; max negative 32 bit integer
    if 'max' in rule:
      max_val = rule['max']
    else:
      max_val = 2**31 - 1     # 2147483647; max positive 32 bit integer
    return str(int(round(random.uniform(min_val, max_val), 0)))


  def generate_float(self, key, rule):
    if 'min' in rule:
      min_val = rule['min']
    else:
      min_val = 0
    if 'MAX' in rule:
      max_val = rule['max']
    else:
      max_val = 1
    value = round(random.uniform(min_val, max_val), 0)
    if 'decimals' in rule:
      decimals = rule['decimals']
      return f"{value:.{decimals}f}"
    return str(value)


  def generate_regex(self, key, rule):
    pattern = rule.get('pattern')
    if not pattern:
      raise ValueError("Pattern must be specified for 'regex' type.")
    return rstr.xeger(pattern)  # Gebruik rstr om een string op basis van regex te genereren
