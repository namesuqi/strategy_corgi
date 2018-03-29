#!/usr/bin/python
# coding=utf-8
# author: Su Qi

from libs.kibana_show_log.kibana_analyse_log import *
from libs.kibana_show_log.push_strategy_log import *
from multiprocessing import Process
import shutil

if __name__ == '__main__':
    shutil.rmtree(LOGS_PATH)
    os.mkdir(LOGS_PATH)

    monitors_for_mysql_and_redis = [
        monitor_combine_parameter,
        monitor_lsm_free,
        read_push_strategy_log,
        monitor_seed_table_file_done,
        monitor_p2p_ratio
    ]

    for monitor in monitors_for_mysql_and_redis:
        p = Process(target=monitor, args=())
        p.daemon = True
        p.start()
    time.sleep(60 * 60 * 24 * 31)

