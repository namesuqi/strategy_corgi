#!/usr/bin/python
# coding=utf-8
# Live sdk_directional_task_live report monitor

from libs.report.report_monitor import *


class LiveDirectionTaskReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(LiveDirectionTaskReportMonitor, self).__init__()
        self.topic = TOPIC_LIVE_DIRECTIONAL_TASK
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "sdk_directional_task_live",
            "file_id": str(item['file_id']),
            "peer_id": str(item['peer_id']),
            "timestamp": long(item['timestamp']),
            "operation": str(item['operation'])
        }
