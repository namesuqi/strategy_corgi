#!/usr/bin/python
# coding=utf-8
# live lf_report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.live_seeds import *


# live online sdk report live_report
class LiveLFReportTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(LiveLFReportTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Live_Seed
        self.topic = TOPIC_LIVE_LF_REPORT
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        return {"topic": self.topic,
                "timestamp": int(time.time() * 1000),
                "ssid": result.ssid,
                "peer_id": result.peer_id,
                "version": result.version,
                "country": result.country,
                "province_id": result.province_id,
                "city_id": result.city_id,
                "isp_id": result.isp_id,
                "file_id": result.file_id,
                "cppc": result.cppc,
                "operation": result.operation,
                "upload": result.upload,
                "download": result.download
                }
