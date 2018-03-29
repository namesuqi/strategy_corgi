#!/usr/bin/python
# coding=utf-8
# live_peer_info report simulator


from libs.simulator.topic_simulator import *
from libs.module.onlines import *


# online sdk report vod_peer_info
class VodPeerInfoTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodPeerInfoTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Online
        self.topic = TOPIC_PEER_INFO
        self.review_duration = 600000

    def create_topic_data(self, result, **kwargs):
        return {
            "topic": self.topic,
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
