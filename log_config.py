import logging
import os
import datetime


"""
To use logging import log_config in file and call 
        logger = logging.getLogger(__name__)
Use logger.debug(message) to log message to log file
Use logger.info(message) to log to console as well as log files
"""
LOG_FORMAT = "%(levelname)s     :%(asctime)s %(message)s"
LOG_LEVEL = logging.DEBUG #for all data to be writen to log
CONSOLE_LEVEL = logging.INFO# for all data to be printed to user
LOG_FILENAME = f'ptServerCLI_{os.environ.get("USER")}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.log'

logging.basicConfig(level = LOG_LEVEL,
                    format = LOG_FORMAT,
                    filename = LOG_FILENAME,
                    filemode='w')

console_handler = logging.StreamHandler()
console_handler.setLevel(CONSOLE_LEVEL)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.getLogger().addHandler(console_handler)