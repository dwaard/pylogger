import logging
from colorama import Fore, Back, Style

class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that uses colorama to format log messages for
    different logging levels with different color settings
    """
    COLORS = {
        logging.DEBUG: Fore.LIGHTBLACK_EX,
        logging.INFO: Fore.WHITE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Back.RED + Fore.WHITE,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        message = super().format(record)
        return f"{color}{message}{reset}"
