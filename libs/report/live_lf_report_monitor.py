#!/usr/bin/python
# coding=utf-8
# Live lf_report report monitor

from libs.report.report_monitor import *


class LiveLFReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(LiveLFReportMonitor, self).__init__()
        self.topic = TOPIC_LIVE_LF_REPORT
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("lf_report"),
            "timestamp": long(item['timestamp']),
            "peer_id": str(item['peer_id']),
            "version": str(item['version']),
            "country": str(item['country']),
            "province_id": str(item['province_id']),
            "city_id": str(item['city_id']),
            "isp_id": str(item['isp_id']),
            "file_id": str(item['file_id']),
            "cppc": int(item['cppc']),
            "operation": str(item['operation']),
            "upload": long(item['upload']),
            "download": long(item['download']),
            "ssid": str(item['ssid'])
            # "lfsid": str(item['lfsid']),
            # "uid_index": str(item['uid_index'])
        }
