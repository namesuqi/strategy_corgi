#!/usr/bin/python
# coding=utf-8
# vod_sdk_file_status report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.seeds import *


# online sdk report vod_sdk_file_status
class VodSDKFileStatusTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodSDKFileStatusTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Seed
        self.topic = TOPIC_FILE_STATUS
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        return {
            "topic": self.topic,
            "peer_id": result.peer_id,
            "file_id": result.file_id,
            "timestamp": int(time.time() * 1000),
            "file_status": result.file_status
        }
