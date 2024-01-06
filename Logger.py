import logging
import urllib3
from colorama import Fore, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        log_message = super().format(record)
        return self.COLORS.get(record.levelname, Fore.WHITE) + log_message + Style.RESET_ALL

colored_formatter = ColoredFormatter('[%(asctime)s]> %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setFormatter(colored_formatter)

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)