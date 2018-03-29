#!/usr/bin/python
# coding=utf-8
# livepush_system_occupancy_monitor report simulator


from libs.simulator.topic_simulator import *
from config import push_review_duration
from libs.module.live_push import *


# live_push report system_occupancy_monitor
class LivePushSystemOccupancyMonitorTopicSimulator(TopicSimulator):
    def __init__(self, log):
        super(LivePushSystemOccupancyMonitorTopicSimulator, self).__init__()
        self.log = log
        self.table_name = Live_Push
        self.topic = TOPIC_PUSH_SYSTEM_OCCUPANCY_MONITOR
        self.review_duration = push_review_duration

    def create_topic_data(self, result, **kwargs):
        return {"topic": self.topic,
                "timestamp": int(time.time() * 1000),
                "cpu_load_1m": result.cpu_load_1m,
                "cpu_count": result.cpu_count,
                "puff_thread_count": result.puff_thread_count,
                "supp_thread_count": result.supp_thread_count,
                "livepush_cpu_used_percentage": result.livepush_cpu_used_percentage,
                "livepush_mem_used_percentage": result.livepush_mem_used_percentage,
                "mem_total": result.mem_total,
                "mem_used": result.mem_used,
                "livepush_version": result.livepush_version,
                "host_id": result.host_id,
                }
