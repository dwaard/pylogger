import sys, os, argparse
from dotenv import load_dotenv
import logging
import json
import colorama
from bsetltools.ColoredFormatter import ColoredFormatter
from datetime import datetime
from pathlib import Path


def init():
  colorama.init()
  # Load the .env to environment variables
  load_dotenv(override=True)
  parser = argparse.ArgumentParser(description="Processing command line parameters.")
  # Configure command line arguments
  parser.add_argument('-v', '--verbose', action='count', default=0, help="Increase verbosity of output (use -v up to -vvv)")

  # Parse the arguments
  args = parser.parse_args()

  # Configure the logging
  configure_logging(args.verbose)

  # Add them to the OS environment variables
  if args.verbose > 2:
    logging.debug('Writing command line arguments to environment variables')
  for key, value in vars(args).items():
    if value is not None:
      env_key = key.upper()
      env_val = str(value)
      if args.verbose > 2:
        logging.debug(f"{env_key} => {env_val}")
      os.environ[env_key] = env_val

  if args.verbose > 2:
    logging.debug("Loggen van alle environment-variabelen:")
    for key in sorted(os.environ):
      value = os.environ[key]
      logging.debug(f"{key} = {value}")

  sys.excepthook = handle_exception
  return args


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Laat ctrl+C gewoon het programma stoppen zonder logging
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))


def buildTargetFilename(filetemplate, timestamp_format="%d-%m-%Y_%H_%M_%S", delimiter='_'):
  """Creates a filename that includes a formatted timestamp between its stem and suffix"""
  # Create the timestamp
  timestamp = datetime.now().strftime(timestamp_format)
  # Use Path to breakup the filename
  path = Path(filetemplate)
  filename = path.with_name(f"{path.stem}{delimiter}{timestamp}{path.suffix}")
  return filename


def configure_logging(verbosity: int):
  """Set the logging level based on verbosity."""
  if verbosity >= 2:
    log_level = logging.DEBUG
  elif verbosity == 1:
    log_level = logging.INFO
  else:
    log_level = logging.WARNING

  logging.captureWarnings(True)

  # Haal LOG_OUTPUT op uit environment, standaard naar stdout
  log_output = os.getenv('LOG_OUTPUT', 'stdout').lower()

  # Root logger
  logger = logging.getLogger()
  logger.setLevel(log_level)

  # Verwijder bestaande handlers (voor herhaalbare configuratie)
  logger.handlers.clear()

  log_warning = ""
  if log_output not in ('stdout', 'file', 'both'):
    log_warning = f"Unknown LOG_OUTPUT value: {log_output}, deferred to stdout."
    log_output = 'stdout'

  debug_messages = []
  if log_output in ('stdout', 'both'):
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    format_str = os.getenv('LOG_STDOUT_FORMAT', '%(message)s')
    formatter = ColoredFormatter(format_str)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    debug_messages.append('Added stdout log handler')

  if log_output in ('file', 'both'):
    filename = os.getenv('LOG_FILE_NAME', 'data/log.txt')
    file_handler = logging.FileHandler(filename)
    format = os.getenv('LOG_FILE_FORMAT', '[%(asctime)s] [%(levelname)s] %(message)s')
    formatter = logging.Formatter(format)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    debug_messages.append('Added file log handler')

  # Log messages regarding logging configuration AFTER logging is configured
  if log_warning != "":
    logging.warning(log_warning)

  for debug_message in debug_messages:
    logging.debug(debug_message)
      
