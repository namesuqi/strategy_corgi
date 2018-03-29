#!/usr/bin/python
# coding=utf-8
# Base class for topics

import time
import json
import redis
import math
from libs.const.topics import *
from libs.const.redis import *
from libs.database.mysql_orm import *
from libs.const.config import flow


class TopicSimulator(object):
    def __init__(self):
        self.log = None
        self.table_name = None
        self.topic = None
        self.review_duration = None

    def create_topic_data(self, result, **kwargs):
        return None

    @staticmethod
    def redis_publisher(redis_host, redis_port, topic, datas):
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        for data in datas:
            r.publish(topic, data)

    def run(self):
        orm = MysqlORM()
        per_peer_p2p_download = 0
        per_peer_cdn_download = 0
        per_seed_download = 0
        per_seed_upload = 0
        while True:
            # from simulator import ret_mutex
            # mutex = ret_mutex()
            # mutex.acquire()
            start_time = time.time()

            if self.topic == TOPIC_FLOW:
                per_peer_p2p_download, per_peer_cdn_download, per_seed_download, per_seed_upload = flow()

            try:

                results = orm.session.query(self.table_name).all()
                orm.session.close()
                self.log.logger.info("Topic:{2}, table:{0}, item number:{1} =======================================".
                                     format(self.table_name, len(results), self.topic))

                section_count = 100
                if 0 < len(results) <= 70:
                    section_count = 1

                if len(results) > 0:
                    # 分阶段处理,平摊处理时间, 分成100段
                    total_time = self.review_duration  # second
                    elements_each_section = len(results) / (section_count * 1.0)
                    time_each_section = total_time / (section_count * 1.0)
                    elements_each_section = int(math.ceil(elements_each_section))

                    for i in range(section_count):
                        start_index = i * elements_each_section
                        n = i + 1
                        end_index = n * elements_each_section

                        messages = list()
                        for result in results[start_index: end_index]:
                            if self.topic == TOPIC_FLOW:
                                data = self.create_topic_data(result, per_peer_p2p_download=per_peer_p2p_download,
                                                              per_peer_cdn_download=per_peer_cdn_download,
                                                              per_seed_download=per_seed_download,
                                                              per_seed_upload=per_seed_upload)
                            else:
                                data = self.create_topic_data(result)
                            message = json.dumps(data)
                            messages.append(message)
                        self.redis_publisher(REDIS_HOST, REDIS_PORT, self.topic, messages)
                        self.log.logger.info("Topic:{topic}, start: {start}, end: {end}, length:{length}".format(
                            topic=self.topic, start=start_index, end=end_index, length=len(messages)))

                        now = time.time()
                        # time compensate
                        if now - start_time < n * time_each_section:
                            duration = n * time_each_section - (now - start_time)
                            time.sleep(duration)

                    end_time = time.time()
                    self.log.logger.info(end_time - start_time)
                else:
                    time.sleep(self.review_duration)

            except Exception as e:
                self.log.logger.info("review {0} exception".format(self.table_name))
                self.log.logger.info(e.message)
                orm.session.close()
            finally:
                pass
            # mutex.release()
            # time.sleep(self.review_duration)
