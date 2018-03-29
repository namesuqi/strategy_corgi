#!/usr/bin/python
# coding=utf-8
# livepush_acl report simulator


from libs.simulator.topic_simulator import *
from config import push_review_duration
from libs.module.live_push import *


# live_push report livepush_acl
class LivePushAclTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(LivePushAclTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Live_Push
        self.topic = TOPIC_PUSH_ACL
        self.review_duration = push_review_duration

    def create_topic_data(self, result, **kwargs):
        return {"topic": self.topic,
                "timestamp": int(time.time() * 1000),
                "event": result.event,
                "livepush_ip": result.ip,
                "reason": result.reason
                }
