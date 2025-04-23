import os
import glob
import logging

class MultiFileSource:

  def __init__(self, folder, pattern="*", sort=False, verbosity=0):
    if verbosity > 0:
      logging.info(f"MultiFileSource: starting")
    self.folder = folder
    self.pattern = pattern
    self.sort = sort
    self.verbosity = verbosity

    # Vind alle bestanden die overeenkomen met het patroon
    search_path = os.path.join(folder, pattern)
    if verbosity > 1:
      logging.debug(f"MultiFileSource: searching {search_path}")
    self.files = glob.glob(search_path)
    if verbosity > 1:
      logging.debug(f"MultiFileSource: reading files {self.files}")

    if sort:
      self.files.sort()

    self.file_index = 0
    self.current_file = None
    self.current_lines = []
    self.line_index = 0

  def __iter__(self):
    return self

  def __next__(self):
    while True:
      if self.current_file is None:
        if self.file_index >= len(self.files):
          raise StopIteration

        self.file_path = self.files[self.file_index]
        self.file_index += 1

        if self.verbosity > 1:
          logging.debug(f"MultiFileSource: opening {self.file_path}")
        with open(self.file_path, "r") as f:
          self.current_lines = f.readlines()

        self.line_index = 0
        self.current_file = self.file_path

      if self.line_index < len(self.current_lines):
        line = self.current_lines[self.line_index]
        self.line_index += 1
        line = line.strip()
        if self.verbosity > 2:
          logging.debug(f"MultiFileSource: read '{line}' from {self.file_path}")
        return line
      else:
        self.current_file = None  # Ga door naar het volgende bestand
