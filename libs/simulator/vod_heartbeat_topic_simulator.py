#!/usr/bin/python
# coding=utf-8
# vod_heartbeat report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.module.onlines import *


# online sdk report vod_heartbeat
class VodHeartbeatTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodHeartbeatTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Online
        self.topic = TOPIC_HEARTBEAT
        # push_download_bandwidth, seed_download_bandwidth, sdk_review_duration, push_review_duration = read_config()
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
                "stun_ip": result.stun_ip,
                "isp_id": result.isp_id,
                "province_id": result.province_id
                }
