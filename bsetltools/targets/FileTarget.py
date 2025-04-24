class FileTarget:
  """
  A simple example class with a constructor and destructor.
  """

  def __init__(self, *args, serializer=None, verbosity=0, **kwargs):
    """
    Constructor that initializes the object with a name.
    
    Args:
      name (str): The name to assign to the object.
    """
    self.verbosity = verbosity
    self.file = open(*args, **kwargs)
    self.serializer = serializer


  def write(self, item):
    """
    Write the item to this target
    """
    if self.serializer is not None:
      item = self.serializer.serialize(item.copy())
    self.file.write(str(item))
    self.file.write('\n')
    self.file.flush()


  def __del__(self):
    """
    Destructor that prints a message when the object is destroyed.
    """
    self.file.close()
