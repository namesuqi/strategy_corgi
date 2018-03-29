#!/usr/bin/python
# coding=utf-8
# push_lsm report monitor

from libs.report.report_monitor import *


class PushLsmReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(PushLsmReportMonitor, self).__init__()
        self.topic = TOPIC_PUSH_LSM
        self.write_num = PUSH_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("vod_push_lsm"),
            "timestamp": long(item['timestamp']),
            "push_id": str(item['push_id']),
            "push_ip": str(item['push_ip']),
            "lsm_free": long(item['lsm_free']),
            "disk_size": long(item['disk_size']),
            "lsm_used": long(item['lsm_used'])
        }
