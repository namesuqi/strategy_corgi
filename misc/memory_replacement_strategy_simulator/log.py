# record sdks behavior
import logging
from logging.handlers import RotatingFileHandler


class Log(object):
    def __init__(self, log_name, log_address, level=logging.DEBUG):
        self.logger = logging.getLogger(log_name)
        formatter = logging.Formatter('%(message)s')
        file_handler = RotatingFileHandler(log_address, maxBytes=100*1024*1024,
                                           backupCount=10)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(level)


