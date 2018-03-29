# -*- coding: utf-8 -*-
# author: zeng yuetian

import logging
import sys


# @singleton
class Log(object):

    def __init__(self, app, log, level=logging.DEBUG):
        # get logger instant，return root logger if param is null
        self.logger = logging.getLogger(app)

        # logger output format
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

        # log file
        file_handler = logging.FileHandler(log)
        file_handler.setFormatter(formatter)

        # console log
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = formatter

        # add log handler for logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # lowest level
        self.logger.setLevel(level)



