#!/usr/bin/python
# coding=utf-8
# vod_sdk_flow(seed) report simulator


from libs.simulator.topic_simulator import *
from config import sdk_review_duration
from libs.const.config import OPERATION, PLAY_TYPE, ERROR_TYPE
from libs.module.seed_pool import *


# online sdk report vod_sdk_flow(seed)
class VodSeedFlowTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(VodSeedFlowTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Seed_pool
        self.topic = TOPIC_FLOW
        self.review_duration = sdk_review_duration

    def create_topic_data(self, result, **kwargs):
        print "seed_download", kwargs['per_seed_download'], "seed_upload", kwargs["per_seed_upload"]
        return {
            "topic": self.topic,
            "peer_id": result.peer_id,
            "public_ip": result.public_ip,
            "isp_id": result.isp_id,
            "province_id": result.province_id,
            "duration": self.review_duration,
            "file_id": result.file_id,
            "timestamp": int(time.time() * 1000),
            "seeds_download": kwargs['per_seed_download'],
            "seeds_upload": kwargs['per_seed_upload'],
            "cdn_download": 0,
            "p2p_download": 0,
            "operation": OPERATION,
            "play_type": PLAY_TYPE,
            "error_type": ERROR_TYPE
        }
