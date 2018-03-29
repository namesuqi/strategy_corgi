#!/usr/bin/python
# coding=utf-8
# author: Su Qi

from libs.kibana_show_log.kibana_analyse_log import *
from libs.kibana_show_log.read_kafka_task import *
from libs.kibana_show_log.push_strategy_log import *
from libs.kibana_show_log.live_read_kafka_task import *
from libs.common.log import *
import threading
import sys

if __name__ == '__main__':
    log = Log("read_task_main.py", MONITOR_PATH + "/read_task_main.log")
    path_exists(LOGS_PATH)
    online_combine_log = LOGS_PATH + "/online_combine.log"
    fil = open(online_combine_log, "w")

    if sys.argv[1] == "vod":
        monitors_for_kafka = [
            monitor_sdk_download_task_channel,
            monitor_sdk_delete_task_channel,
            monitor_push_prefetch_task_channel,
            monitor_push_delete_task_channel
        ]

    if sys.argv[1] == "live":
        monitors_for_kafka = [monitor_sdk_directional_task_channel]

    for monitor in monitors_for_kafka:
        time.sleep(2)
        t = threading.Thread(target=monitor, args=(log,))
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
