# calculate the time spent in all aspects
# author: myn


import threading
import time
from libs.common.log import Log
from libs.common.path import MONITOR_PATH
from libs.database.handle_kafka import search_schema, new_consumer, \
    read_logs_from_kafka
from libs.database.mysql_orm import MysqlORM
from libs.module.seeds import Seed
from libs.module.vod_push_file import Vod_Push_File
from libs.const.topics import *


def get_task_prefetch_cost():
    global time_1
    valve = 0
    schemas = search_schema([TOPIC_TASK_SDK_DOWNLOAD,
                             TOPIC_TASK_SDK_DELETE,
                             TOPIC_TASK_PUSH_PREFETCH,
                             TOPIC_TASK_PUSH_DELETE])
    new_consumers = new_consumer([TOPIC_TASK_SDK_DOWNLOAD,
                                 TOPIC_TASK_SDK_DELETE,
                                 TOPIC_TASK_PUSH_PREFETCH,
                                 TOPIC_TASK_PUSH_DELETE],
                                 'Kiroff_time',
                                 '192.168.4.230:9092')
    time_0 = time.time()
    log.logger.info('push prefetch start time:{0}'.format(time_0))
    while True:
        received_all_tasks = read_logs_from_kafka(new_consumers, schemas)
        if valve == 0 and len(received_all_tasks) != 0:
            for task in received_all_tasks:
                if len(task[2]) == 11:
                    valve = 1
                    time_1 = time.time()
                    log.logger.info(
                        'push get task prefetch files{0}, push cost {1} '
                        's to get prefetch task '.format(
                            time_1, time_1 - time_0))
                    break


def push_prefetch_finish(orm):
    valve = 0
    while True:
        done_list = orm.session.query(Vod_Push_File).filter_by(
            behavior='in').all()
        if len(done_list) != 0 and valve == 0:
            valve = 1
            time_10 = time.time()
            log.logger.info(
                'push down file finish cost {0}s'.format(time_10))


def seed_get_file_cost(orm, ):
    time_2 = time.time()
    global time_3
    global time_4
    global time_5
    global time_6
    global time_7
    global time_8
    log.logger.info('give seed start time:{0}'.format(time_2))
    while True:
        time_f = time.time()
        done_list = orm.session.query(Seed).filter_by(file_status='done').all()
        if len(done_list) == 100:
            time_3 = time.time()
            log.logger.info('100 seed done cost :{0}s'.format(time_3 - time_2))
        if len(done_list) == 200:
            time_4 = time.time()
            log.logger.info('200 seed done cost :{0}s'.format(time_4 - time_3))
        if len(done_list) == 300:
            time_5 = time.time()
            log.logger.info('300 seed done cost :{0}s'.format(time_5 - time_4))
        if len(done_list) == 400:
            time_6 = time.time()
            log.logger.info('400 seed done cost :{0}s'.format(time_6 - time_5))
        if len(done_list) == 500:
            time_7 = time.time()
            log.logger.info('500 seed done cost :{0}s'.format(time_7 - time_6))
        if len(done_list) == 600:
            time_8 = time.time()
            log.logger.info('600 seed done cost :{0}s'.format(time_8 - time_7))
        if len(done_list) == 700:
            time_9 = time.time()
            log.logger.info('700 seed done cost :{0}s'.format(time_9 - time_8))
        if len(done_list) == 800:
            time_10 = time.time()
            log.logger.info(
                '800 seed done cost :{0}s'.format(time_10 - time_2))
        if len(done_list) > 800 or time_f - time_2 > 5400:
            break
        time.sleep(0.5)


if __name__ == '__main__':
    orm = MysqlORM()
    log = Log("time_calculate", MONITOR_PATH + "/time_calculate.log")
    t1 = threading.Thread(target=get_task_prefetch_cost, args=())
    t1.start()
    t2 = threading.Thread(target=seed_get_file_cost, args=(orm,))
    t2.start()
    t3 = threading.Thread(target=push_prefetch_finish, args=(orm,))
    t3.start()

