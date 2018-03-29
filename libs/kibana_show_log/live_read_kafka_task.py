#!/usr/bin/python
# coding=utf-8
# read push tasks from kafka and write to logs for ELK analysis
# author: Su Qi

from libs.common.path import *
from libs.const.topics import *
import json
from libs.database.handle_kafka import *


def monitor_sdk_directional_task_channel(log):
    sdk_download_log = LOGS_PATH + "/{0}.log".format(TOPIC_LIVE_DIRECTIONAL_TASK)
    fil = open(sdk_download_log, "w")
    log.logger.info('open sdk_directional_task_live.log')
    schemas = search_schema([TOPIC_LIVE_DIRECTIONAL_TASK])
    new_consumers = new_consumer([TOPIC_LIVE_DIRECTIONAL_TASK],
                                 'sdk_task',
                                 KAFKA_HOSTS)
    download_num = 0
    delete_num = 0
    while True:
        read_sdk_download_tasks = read_logs_from_kafka(new_consumers, schemas)
        for sdk_task in read_sdk_download_tasks:
            if "download" == sdk_task[2]["operation"]:
                download_num += 1
                sdk_task_info = sdk_task[2]
                sdk_download_json = json.dumps(sdk_task_info)
                fil.write(sdk_download_json + "\n")
            fil.flush()
            log.logger.info('read_sdk_download_task_live {} items'.format(download_num))
            if "delete" == sdk_task[2]["operation"]:
                delete_num += 1
                sdk_task_info = sdk_task[2]
                sdk_delete_json = json.dumps(sdk_task_info)
                fil.write(sdk_delete_json + "\n")
            fil.flush()
            log.logger.info('read_sdk_delete_task_live {} items'.format(delete_num))
    time.sleep(10)

if __name__ == '__main__':
    monitor_sdk_directional_task_channel()