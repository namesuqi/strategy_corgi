#!/usr/bin/python
# coding=utf-8
# vod_sdk_flow(peer) report simulator


from libs.simulator.topic_simulator import *
from config import *
from libs.module.peers import *


# online sdk report vod_sdk_flow
class VodPeerFlowTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodPeerFlowTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Peer
        self.topic = TOPIC_FLOW
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        print "peer_cdn_download", kwargs['per_peer_cdn_download'], "peer_p2p_download", kwargs['per_peer_p2p_download']
        return {
            "topic": self.topic,
            "peer_id": result.peer_id,
            "public_ip": result.public_ip,
            "isp_id": result.isp_id,
            "province_id": result.province_id,
            "duration": result.duration,
            "file_id": result.file_id,
            "timestamp": int(time.time() * 1000),
            "seeds_download": 0,
            "seeds_upload": 0,
            "cdn_download": kwargs['per_peer_cdn_download'],
            "p2p_download": kwargs['per_peer_p2p_download'],
            "operation": result.operation,
            "play_type": result.play_type,
            "error_type": result.error_type
        }
