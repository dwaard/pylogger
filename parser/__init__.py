from dateutil.parser import parse


def build():
  return BasicParser()


class BasicParser:
  """
  Basic parser that only allows fixed format:

  [timestamp;float;float;float;float]
  """

  def parse(self, line):
    valid = False
    # split the string using the delimiter
    data = line.rstrip().split(';')
    # each line is aways expected to have 5 elements
    if (len(data) == 5):
      try:
        data[0] = parse(data[0])
        for index in range(1, len(data)):
            data[index] = float(data[index])
        valid = True
      except ValueError:
        valid = False
    return valid, data