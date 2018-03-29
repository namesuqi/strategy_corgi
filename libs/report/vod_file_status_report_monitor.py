#!/usr/bin/python
# coding=utf-8
# file_status report monitor

from libs.report.report_monitor import *


class VodFileStatusReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(VodFileStatusReportMonitor, self).__init__()
        self.topic = TOPIC_FILE_STATUS
        self.write_num = FILE_STATUS_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "vod_sdk_file_status",
            "timestamp": long(item['timestamp']),
            "peer_id": str(item['peer_id']),
            "file_id": str(item['file_id']),
            # "downloading", "done", "none", "interrupt"
            "file_status": str(item['file_status'])
        }
