# -*- coding: utf-8 -*-
# author: zengyuetian
# write log with multi-thread

import threading
import time
from libs.common.log import *
from libs.common.path import *


def thread_1():
    log.logger.info('this is message from thread1')
    time.sleep(1)


def thread_2():
    log.logger.info('this is message from thread2')
    time.sleep(1)


if __name__ == "__main__":
    # get log.logger instance，if param is NULL then return root log.logger
    log = Log("thread_log", MONITOR_PATH + "/test.log")

    # different level log
    log.logger.debug('this is debug info')
    log.logger.info('this is information')
    log.logger.warn('this is warning message')
    log.logger.error('this is error message')
    log.logger.fatal('this is fatal message, it is same as log.logger.critical')
    log.logger.critical('this is critical message')

    # 2016-10-08 21:59:19,493 INFO    : this is information
    # 2016-10-08 21:59:19,493 WARNING : this is warning message
    # 2016-10-08 21:59:19,493 ERROR   : this is error message
    # 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as log.logger.critical
    # 2016-10-08 21:59:19,493 CRITICAL: this is critical message

    threads = [thread_1, thread_2]
    for monitor in threads:
        t = threading.Thread(target=monitor, args=())
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

        # remove log handler
        # log.logger.removeHandler(file_handler)
