#!/usr/bin/python
# coding=utf-8
# vod_all_files report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.files import *


# online sdk report vod_all_files
class VodAllFilesTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodAllFilesTopicSimulator, self).__init__()
        self.log = log
        self.table_name = File
        self.topic = TOPIC_VOD_ALLFILES
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        return {
            "topic": self.topic,
            "file_id": result.file_id,
            "file_size": result.file_size,
            "url": result.url,
            "timestamp": int(time.time() * 1000),
            "ppc": result.ppc,
            "cppc": result.cppc,
            "piece_size": result.piece_size
        }
