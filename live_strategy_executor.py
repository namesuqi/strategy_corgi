#!/usr/bin/python
# coding=utf-8
# 1.read strategy tasks from kafka
# 2.execute tasks and write results to mysql
# author = Su Qi

from libs.database.handle_kafka import *
from libs.const.topics import *
from libs.const.config import KAFKA_ADDRESS
from libs.strategy_executor.deal_live_strategy_task import *
from libs.common.log import *
from libs.common.path import *

log = Log("live_strategy_executor", MONITOR_PATH + "/live_strategy_executor.log")


def write_live_tasks_info_to_mysql():
    orm = MysqlORM()
    schemas = search_schema([TOPIC_LIVE_DIRECTIONAL_TASK])
    new_consumers = new_consumer([TOPIC_LIVE_DIRECTIONAL_TASK],
                                 'live_task',
                                 KAFKA_ADDRESS)
    while True:
        read_live_directional_tasks = read_logs_from_kafka(new_consumers, schemas)
        for task in read_live_directional_tasks:
            task_info = task[2]
            file_id = task_info['file_id']
            peer_id = task_info['peer_id']
            operation = task_info['operation']

            live_info_online = orm.session.query(Live_Online).filter_by(peer_id=peer_id).all()
            orm.session.close()

            # sdk in table online
            if len(live_info_online) > 0:
                log.logger.info('seed operation {0} at {1}'.format(operation, time.time()))
                deal_live_strategy_tasks(task_info, peer_id, file_id)


if __name__ == '__main__':
    write_live_tasks_info_to_mysql()
