#!/usr/bin/python
# coding=utf-8
# Base class for monitors

import redis
import json
from libs.common.path import *
from libs.const.topics import *
from libs.const.redis import *
from libs.database.handle_kafka import *
from config import push_write_num, file_write_num, file_status_write_number, sdk_write_number

PUSH_WRITE_NUMBER = push_write_num
FILE_WRITE_NUMBER = file_write_num
FILE_STATUS_WRITE_NUMBER = file_status_write_number
SDK_WRITE_NUMBER = sdk_write_number


class ReportMonitor(object):
    
    def __init__(self):
        self.log = None
        self.write_num = None
        self.topic = None

    def create_topic_data(self, item):
        return None

    @staticmethod
    def write_to_kafka(topic, datas, kafka_topic, schema, schema_id):
        write_logs_to_kafka_with_schema(topic, datas, kafka_topic, schema, schema_id)

    def run(self):
        if self.topic != TOPIC_HEARTBEAT and self.topic != TOPIC_VOD_LSM:
            topic_log = LOGS_PATH + "/{0}.log".format(self.topic)
            fil = open(topic_log, "w")
            self.log.logger.info('open {0}.log'.format(self.topic))

        pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        p = r.pubsub()

        client = KafkaClient(hosts=KAFKA_HOSTS)
        kafka_topic = client.topics[self.topic]
        schema, schema_id = get_latest_schema_info(self.topic)

        while True:
            try:
                # read data from redis task list
                p.subscribe(self.topic)
                messages = list()
                num = 0
                for item in p.listen():
                    if 'data' in item:
                        if type(item['data']) is str:
                            num += 1
                            i_item = json.loads(item['data'])
                            topic_data = self.create_topic_data(i_item)

                            # write data to log file
                            messages.append(topic_data)

                            # write to logs and kafka every write_item_num
                            if num % self.write_num == 0 and num != 0:
                                if self.topic != TOPIC_HEARTBEAT and self.topic != TOPIC_VOD_LSM:
                                    for message in messages:
                                        message_json = json.dumps(message)
                                        fil.write(message_json + "\n")
                                    fil.flush()

                                # set level to disable some logs
                                self.log.logger.info(
                                    '[{0}.log]: add {1} items'.format(self.topic, self.write_num))

                                # write data to kafka
                                self.write_to_kafka(self.topic, messages, kafka_topic, schema, schema_id)

                                # show log number to kafka
                                self.log.logger.info(
                                    '[{0}.kafka]: add {1} items'.format(self.topic, self.write_num))
                                # clean list for next write operation
                                messages = list()

                                # time.sleep(1)

            except Exception as e:
                self.log.logger.info("review {0} exception".format(self.topic))
                self.log.logger.info(e.message)
