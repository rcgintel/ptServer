import logging
import os
import datetime

#configure client logger

def get_client_logger():
    """ 
            client_logger.debug("This is a log message")
    Use client_logger.debug(message) to log message to log file
    Use client_logger.info(message) to log to console as well as log files
    """
    if "client_logger" not in logging.Logger.manager.loggerDict:

        CLIENT_LOG_FORMAT = "%(levelname)s     :%(asctime)s %(message)s"
        CLIENT_LOG_LEVEL = logging.DEBUG #for all data to be writen to log
        CLIENT_CONSOLE_LEVEL = logging.INFO# for all data to be printed to user
        CLIENT_LOG_FILENAME = f'ptServerCLI_{os.environ.get("USER")}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.log'


        client_logger = logging.getLogger('client_logger')
        client_logger.setLevel(CLIENT_LOG_LEVEL)
        client_file_handler = logging.FileHandler(CLIENT_LOG_FILENAME,mode = 'w')
        client_file_handler.setLevel(CLIENT_LOG_LEVEL)
        client_file_formatter = logging.Formatter(CLIENT_LOG_FORMAT)
        client_file_handler.setFormatter(client_file_formatter)
        client_logger.addHandler(client_file_handler)

        client_console_handler = logging.StreamHandler()
        client_console_handler.setLevel(CLIENT_CONSOLE_LEVEL)
        client_console_formatter = logging.Formatter(CLIENT_LOG_FORMAT)
        client_console_handler.setFormatter(client_console_formatter)
        client_logger.addHandler(client_console_handler)

    else:

        client_logger = logging.getLogger('client_logger')

    return client_logger

#configure server logger
def get_server_logger():
    """
            server_logger.debug("This is a log message")
    Use server_logger.debug(message) to log message to log files
    Use server_logger.info(message) to log messager to console as well as log files
    """
    if 'server_logger' not in logging.Logger.manager.loggerDict:

        SERVER_LOG_FORMAT = "%(levelname)s     :%(asctime)s %(message)s"
        SERVER_LOG_LEVEL = logging.DEBUG #for all data to be writen to log
        SERVER_CONSOLE_LEVEL = logging.INFO# for all data to be printed to user
        SERVER_LOG_FILENAME = f'ptServerMachineSpawn_{os.environ.get("USER")}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.log'


        server_logger = logging.getLogger('server_logger')
        server_logger.setLevel(SERVER_LOG_LEVEL)
        server_file_handler = logging.FileHandler(SERVER_LOG_FILENAME, mode = "w")
        server_file_handler.setLevel(SERVER_LOG_LEVEL)
        server_formatter = logging.Formatter(SERVER_LOG_FORMAT)
        server_file_handler.setFormatter(server_formatter)
        server_logger.addHandler(server_file_handler)

        server_console_handler = logging.StreamHandler()
        server_console_handler.setLevel(SERVER_CONSOLE_LEVEL)
        server_console_handler.setFormatter(server_formatter)
        server_logger.addHandler(server_console_handler)

    else:

        server_logger = logging.getLogger('server_logger')

    return server_logger