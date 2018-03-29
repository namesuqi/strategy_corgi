#!/usr/bin/python
# coding=utf-8
# Live_push livepush_acl report monitor

from libs.report.report_monitor import *


class LivePushMonitorLog(ReportMonitor):
    def __init__(self, log):
        super(LivePushMonitorLog, self).__init__()
        self.topic = TOPIC_PUSH_ACL
        self.write_num = PUSH_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "livepush_acl",
            "timestamp": long(item['timestamp']),
            "event": str(item['event']),
            "livepush_ip": str(item['livepush_ip']),
            "reason": str(item['reason'])
        }
