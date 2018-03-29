#!/usr/bin/python
# coding=utf-8
# live_heartbeat report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.live_onlines import *


# live online sdk report heartbeat
class LiveHeartbeatTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(LiveHeartbeatTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Live_Online
        self.topic = TOPIC_LIVE_HEARTBEAT
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        return {"topic": self.topic,
                "peer_id": result.peer_id,
                "sdk_version": result.sdk_version,
                "public_ip": result.public_ip,
                "public_port": result.public_port,
                "private_ip": result.private_ip,
                "private_port": result.private_port,
                "nat_type": result.nat_type,
                "timestamp": int(time.time() * 1000),
                "isp_id": result.isp_id,
                "province_id": result.province_id,
                "ssid": result.ssid,
                "country": result.country,
                "city_id": result.city_id
                }
