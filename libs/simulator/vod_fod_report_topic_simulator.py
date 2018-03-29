#!/usr/bin/python
# coding=utf-8
# vod_fod_report report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.peers import *


# online sdk report vod_fod_report
class VodFodReportTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodFodReportTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Peer
        self.topic = TOPIC_FOD_REPORT
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        return {
            "topic": self.topic,
            "timestamp": int(time.time() * 1000),
            "peer_id": result.peer_id,
            "file_id": result.file_id,
            "file_size": result.file_size,
            "url": result.url,
            "play_type": result.play_type,
            "public_ip": result.public_ip,
            "isp_id": result.isp_id,
            "province_id": result.province_id,
            "ppc": result.ppc,
            "piece_size": result.piece_size,
            "cppc": result.cppc
        }
