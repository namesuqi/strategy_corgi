# coding=utf-8
# __author__ = 'zengyuetian'

import inspect
import os
import sys


def get_root_path():
    """
    get the automatic test framework root directory
    :return:
    """
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    parent_path = os.path.dirname(file_path)
    lib_path = os.path.dirname(parent_path)
    root_path = os.path.dirname(lib_path)
    return root_path


def get_root_parent_path():
    """
    get the parent directory of the automated test framework root
    :return:
    """
    root_parent_path = os.path.dirname(get_root_path())
    return root_parent_path


def get_root_dir_name():
    return os.path.basename(get_root_path())


LOGS_PATH = get_root_path() + "/logs"
MONITOR_PATH = get_root_path() + "/monitor"
MISC_PATH = get_root_path() + "/misc"
REPORT_PATH = get_root_path() + "/report"
SIMULATOR_PATH = get_root_path() + "/simulator_log"


###############################
# Debugging use
###############################
if __name__ == "__main__":
    print get_root_path()
    print get_root_dir_name()



