#!/usr/bin/python
# coding=utf-8
# vod_push_disk_cache report simulator


from libs.simulator.topic_simulator import *
from config import push_review_duration
from libs.module.vod_push_file import *


# online sdk report vod_push_disk_cache
class VodPushDiskCacheTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodPushDiskCacheTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Vod_Push_File
        self.topic = TOPIC_PUSH_DISK
        self.review_duration = push_review_duration

    def create_topic_data(self, result, **kwargs):
        if result.behavior:
            return {
                "topic": self.topic,
                "push_id": result.push_id,
                "push_ip": result.push_ip,
                "file_id": result.file_id,
                "file_size": result.file_size,
                "behavior": result.behavior,
                "universe": True,
                "timestamp": int(time.time() * 1000)
            }
