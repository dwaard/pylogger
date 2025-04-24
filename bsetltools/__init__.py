import sys, os, argparse
from dotenv import load_dotenv
import logging
import json
import colorama
from bsetltools.ColoredFormatter import ColoredFormatter
from datetime import datetime
from pathlib import Path


def init(argparse_initialize_func=None):
  """
  Initializes BSETLtools. It loads environmnent variables and command line 
  arguments into environmnent variables and configures logging.

  Parameters:
    argparse_initialize_func (ArgumentParser): Callback function to enable 
                                               adding custom command line 
                                               options
  """
  # Cache debug, info, warning and error messages because the logging is not
  # configured yet. They are logged after logging is configured.
  debug_messages = []
  info_messages = []
  warning_messages = []
  error_messages = []
  # For the nice colors while printing to the console
  colorama.init()
  # Load the .env into environment variables
  load_dotenv(override=True)

  # Configure argparse for command line arguments
  parser = argparse.ArgumentParser(description="Processing command line parameters.")
  parser.add_argument('-v', '--verbose', action='count', default=0, help="Increase verbosity of output (use -v up to -vvv)")
  if argparse_initialize_func is not None:
    argparse_initialize_func(parser)
  # Parse the arguments
  args = parser.parse_args()
  # Add the parsed args to the OS environment variables. This overwrites
  # potential existing vars intentionally. It makes them highest priority
  if args.verbose > 2:
    logging.debug('Writing command line arguments to environment variables')
  for key, value in vars(args).items():
    if value is not None:
      env_key = key.upper()
      env_val = str(value)
      if args.verbose > 2:
        logging.debug(f"{env_key} => {env_val}")
      os.environ[env_key] = env_val

  # Configure the logging. The logging level is determind by the verbose 
  # setting like so:
  if args.verbose >= 2:
    log_level = logging.DEBUG
  elif args.verbose == 1:
    log_level = logging.INFO
  else:
    log_level = logging.WARNING
  # Make sure logging captures warnings and exceptions
  logging.captureWarnings(True)
  sys.excepthook = capture_exceptions_to_logging
  # Configure the root logger
  logger = logging.getLogger()
  logger.setLevel(log_level)
  # Remove existing handlers (to make the configuration repeatable)
  logger.handlers.clear()
  # Get LOG_OUTPUT from environment, validate and default to stdout
  log_output = os.getenv('LOG_OUTPUT', 'stdout').lower()
  if log_output not in ('stdout', 'file', 'both'):
    warning_messages.append(f"Unknown LOG_OUTPUT value: {log_output}, defaulted to 'stdout'.")
    log_output = 'stdout'
  # Configure the stdout logger
  if log_output in ('stdout', 'both'):
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    format_str = os.getenv('LOG_STDOUT_FORMAT', '%(message)s')
    formatter = ColoredFormatter(format_str)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    debug_messages.append('Added stdout log handler')
  # Configure the file logger
  if log_output in ('file', 'both'):
    filename = os.getenv('LOG_FILE_NAME', '.log/log.txt')
    file_handler = logging.FileHandler(buildTargetFilename(filename))
    format = os.getenv('LOG_FILE_FORMAT', '[%(asctime)s] [%(levelname)s] %(message)s')
    formatter = logging.Formatter(format)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    debug_messages.append('Added file log handler')

  # Log cached messages regarding logging configuration AFTER logging is configured
  for msg in debug_messages:
    logging.debug(msg)
  for msg in info_messages:
    logging.info(msg)
  for msg in warning_messages:
    logging.warning(msg)
  for msg in error_messages:
    logging.error(msg)

  # Finally, return the parsed arguments for convenience
  return args


def capture_exceptions_to_logging(exc_type, exc_value, exc_traceback):
  """
  Callback function for exception hook
  """
  if issubclass(exc_type, KeyboardInterrupt):
    # Laat ctrl+C gewoon het programma stoppen zonder logging
    sys.__excepthook__(exc_type, exc_value, exc_traceback)
    return
  logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))


def buildTargetFilename(filetemplate, timestamp_format="%Y-%m-%d_%H_%M_%S", delimiter='_'):
  """
  Helper function that creates a filename that includes a formatted timestamp 
  between its stem and suffix
  """
  # Create the timestamp
  timestamp = datetime.now().strftime(timestamp_format)
  # Use Path to breakup the filename
  path = Path(filetemplate)
  filename = path.with_name(f"{path.stem}{delimiter}{timestamp}{path.suffix}")
  return filename
      
