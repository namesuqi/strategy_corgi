#!/usr/bin/python
# coding=utf-8
# Live_push system_occupancy_monitor report monitor

from libs.report.report_monitor import *


class LivePushSystemOccupancyMonitor(ReportMonitor):
    def __init__(self, log):
        super(LivePushSystemOccupancyMonitor, self).__init__()
        self.topic = TOPIC_PUSH_SYSTEM_OCCUPANCY_MONITOR
        self.write_num = PUSH_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "system_occupancy_monitor",
            "timestamp": long(item['timestamp']),
            "cpu_load_1m": float(item['cpu_load_1m']),
            "cpu_count": int(item['cpu_count']),
            "puff_thread_count": int(item['puff_thread_count']),
            "supp_thread_count": int(item['supp_thread_count']),
            "livepush_cpu_used_percentage": float(item['livepush_cpu_used_percentage']),
            "livepush_mem_used_percentage": float(item['livepush_mem_used_percentage']),
            "mem_total": long(item['mem_total']),
            "mem_used": long(item['mem_used']),
            "livepush_version": str(item['livepush_version']),
            "host_id": str(item['host_id']),
            # "detail_info": str(item['detail_info'])
        }
