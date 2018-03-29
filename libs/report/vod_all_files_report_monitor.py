#!/usr/bin/python
# coding=utf-8
# all_files report monitor

from libs.report.report_monitor import *


class VodAllFilesReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(VodAllFilesReportMonitor, self).__init__()
        self.topic = TOPIC_VOD_ALLFILES
        self.write_num = FILE_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "vod_all_files",
            "timestamp": long(item['timestamp']),
            "file_size": long(item['file_size']),
            "ppc": int(item['ppc']),
            "cppc": int(item['cppc']),
            "piece_size": int(item['piece_size']),
            "file_id": str(item['file_id']),
            "url": str(item['url']),
            "file_type": str("m3u8")
        }
