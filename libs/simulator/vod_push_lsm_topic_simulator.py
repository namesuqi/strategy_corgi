#!/usr/bin/python
# coding=utf-8
# vod_push_lsm report simulator


from libs.simulator.topic_simulator import *
from config import push_review_duration
from libs.module.vod_push import *


# online sdk report vod_push_lsm
class VodPushLsmTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodPushLsmTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Vod_Push
        self.topic = TOPIC_PUSH_LSM
        self.review_duration = push_review_duration

    def create_topic_data(self, result, **kwargs):

        return {
            "topic": self.topic,
            "push_id": result.push_id,
            "push_ip": result.push_ip,
            "disk_size": result.disk_size,
            "lsm_used": result.lsm_used,
            "lsm_free": result.lsm_free,
            "timestamp": int(time.time() * 1000)
        }
