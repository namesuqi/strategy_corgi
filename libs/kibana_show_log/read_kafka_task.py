#!/usr/bin/python
# coding=utf-8
# read push tasks from kafka and write to logs for ELK analysis
# author: Su Qi

from libs.common.path import *
from libs.const.topics import *
import json
from libs.database.handle_kafka import *


def monitor_sdk_download_task_channel(log):
    sdk_download_log = LOGS_PATH + "/{0}.log".format(TOPIC_TASK_SDK_DOWNLOAD)
    fil = open(sdk_download_log, "w")
    log.logger.info('open sdk_download_task.log')
    schemas = search_schema([TOPIC_TASK_SDK_DOWNLOAD])
    new_consumers = new_consumer([TOPIC_TASK_SDK_DOWNLOAD],
                                 'sdk_download',
                                 KAFKA_HOSTS)
    while True:
        read_sdk_download_tasks = read_logs_from_kafka(new_consumers, schemas)
        if read_sdk_download_tasks is not []:
            for sdk_download_task in read_sdk_download_tasks:
                sdk_task_info = sdk_download_task[2]
                sdk_download_json = json.dumps(sdk_task_info)
                fil.write(sdk_download_json + "\n")
            fil.flush()
        log.logger.info('read_sdk_download_task {} items'.format(len(read_sdk_download_tasks)))
        time.sleep(10)


def monitor_sdk_delete_task_channel(log):
    sdk_delete_log = LOGS_PATH + "/{0}.log".format(TOPIC_TASK_SDK_DELETE)
    fil = open(sdk_delete_log, "w")
    log.logger.info('open sdk_delete_task.log')
    schemas = search_schema([TOPIC_TASK_SDK_DELETE])
    new_consumers = new_consumer([TOPIC_TASK_SDK_DELETE],
                                 'sdk_delete',
                                 KAFKA_HOSTS)
    while True:
        read_sdk_delete_tasks = read_logs_from_kafka(new_consumers, schemas)
        for sdk_delete in read_sdk_delete_tasks:
            sdk_delete_info = sdk_delete[2]
            sdk_delete_json = json.dumps(sdk_delete_info)
            fil.write(sdk_delete_json + "\n")
        fil.flush()
        log.logger.info('read_sdk_delete_task {} items'.format(len(read_sdk_delete_tasks)))
        time.sleep(10)


def monitor_push_prefetch_task_channel(log):
    push_prefetch_log = LOGS_PATH + "/{0}.log".format(TOPIC_TASK_PUSH_PREFETCH)
    fil = open(push_prefetch_log, "w")
    log.logger.info('open push_prefetch_task.log')
    schemas = search_schema([TOPIC_TASK_PUSH_PREFETCH])
    new_consumers = new_consumer([TOPIC_TASK_PUSH_PREFETCH],
                                 'push_prefetch',
                                 KAFKA_HOSTS)
    while True:
        read_push_prefetch_tasks = read_logs_from_kafka(new_consumers, schemas)
        if read_push_prefetch_tasks is not []:
            for push_prefetch in read_push_prefetch_tasks:
                push_prefetch_info = push_prefetch[2]
                push_prefetch_json = json.dumps(push_prefetch_info)
                fil.write(push_prefetch_json + "\n")
            fil.flush()
        log.logger.info('read_push_prefetch_task {} items'.format(len(read_push_prefetch_tasks)))
        time.sleep(10)


def monitor_push_delete_task_channel(log):
    push_delete_log = LOGS_PATH + "/{0}.log".format(TOPIC_TASK_PUSH_DELETE)
    fil = open(push_delete_log, "w")
    log.logger.info('open push_delete_task.log')
    schemas = search_schema([TOPIC_TASK_PUSH_DELETE])
    new_consumers = new_consumer([TOPIC_TASK_PUSH_DELETE],
                                 'push_delete',
                                 KAFKA_HOSTS)
    while True:
        read_push_delete_tasks = read_logs_from_kafka(new_consumers, schemas)
        for push_delete in read_push_delete_tasks:
            push_delete_info = push_delete[2]
            push_delete_json = json.dumps(push_delete_info)
            fil.write(push_delete_json + "\n")
        fil.flush()
        log.logger.info('read_push_delete_task {} items'.format(len(read_push_delete_tasks)))
        time.sleep(10)
