#!/usr/bin/python
# coding=utf-8
# live_report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.live_peers import *


# live online sdk report live_report
class LiveReportTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(LiveReportTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Live_Peer
        self.topic = TOPIC_LIVE_SDK_REPORT
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        return {"topic": self.topic,
                "peer_id": result.peer_id,
                "timestamp": int(time.time() * 1000),
                "ssid": result.ssid,
                "version": result.version,
                "country": result.country,
                "province_id": result.province_id,
                "city_id": result.city_id,
                "isp_id": result.isp_id,
                "file_id": result.file_id,
                "chunk_id": result.chunk_id,
                "operation": result.operation,
                "cdn": result.cdn,
                "p2p": result.p2p,
                "p2penable": True
                }
