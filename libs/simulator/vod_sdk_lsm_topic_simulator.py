#!/usr/bin/python
# coding=utf-8
# vod_sdk_lsm report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.onlines import *


# online sdk report vod_sdk_lsm
class VodSDKLsmTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodSDKLsmTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Online
        self.topic = TOPIC_VOD_LSM
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        return {
            "topic": self.topic,
            "peer_id": result.peer_id,
            "disk_total": result.disk_total,
            "disk_free": result.disk_free,
            "lsm_total": result.lsm_total,
            "lsm_free": result.lsm_free,
            "timestamp": int(time.time() * 1000)
        }
