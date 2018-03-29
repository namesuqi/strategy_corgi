#!/usr/bin/python
# coding=utf-8
# livepush_network_card_flow report simulator


from libs.simulator.topic_simulator import *
from config import push_review_duration
from libs.module.live_push import *


# live_push report network_card_flow
class LivePushNetworkCardFlowTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(LivePushNetworkCardFlowTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Live_Push
        self.topic = TOPIC_PUSH_NETWORK_CARD_FLOW
        self.review_duration = push_review_duration

    def create_topic_data(self, result, **kwargs):
        return {"topic": self.topic,
                "timestamp": int(time.time() * 1000),
                "name": result.name,
                "receive": result.receive,
                "transmit": result.transmit,
                "bandwidth": result.bandwidth,
                "ip": result.ip,
                "host_id": result.host_id,
                }
