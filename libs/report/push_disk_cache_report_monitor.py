#!/usr/bin/python
# coding=utf-8
# push_disk_cache report monitor

from libs.report.report_monitor import *


class PushDiskCacheReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(PushDiskCacheReportMonitor, self).__init__()
        self.topic = TOPIC_PUSH_DISK
        self.write_num = PUSH_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("vod_push_disk_cache"),
            "timestamp": long(item['timestamp']),
            "push_id": str(item['push_id']),
            "push_ip": str(item['push_ip']),
            "universe": item['universe'],
            "file_id": str(item['file_id']),
            "file_size": item['file_size'],
            "behavior": str(item['behavior'])
        }
