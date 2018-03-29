#!/usr/bin/python
# coding=utf-8
# push_prefetch_task report monitor

from libs.report.report_monitor import *


class PushPrefetchTaskReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(PushPrefetchTaskReportMonitor, self).__init__()
        self.topic = TOPIC_PUSH_PREFETCH
        self.write_num = PUSH_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("vod_push_prefetch_task"),
            "timestamp": item['timestamp'],
            "file_id": str(item['file_id']),
            "push_id": str(item['push_id']),
            "push_ip": str(item['push_ip']),
            "file_size": item['file_size'],
            "flag": str(item['flag']),
            "universe": item['universe']
        }
