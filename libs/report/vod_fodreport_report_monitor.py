#!/usr/bin/python
# coding=utf-8
# Vod_fod_report report monitor

from libs.report.report_monitor import *


class VodFodReportReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(VodFodReportReportMonitor, self).__init__()
        self.topic = TOPIC_FOD_REPORT
        self.write_num = FILE_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("vod_fod_report"),
            "timestamp": long(item['timestamp']),
            "peer_id": str(item['peer_id']),
            "file_id": str(item['file_id']),
            "file_size": long(item['file_size']),
            "play_type": str(item['play_type']),
            "ppc": int(item['ppc']),
            "cppc": int(item['cppc']),
            "piece_size": int(item['piece_size']),
            "isp_id": str(item['isp_id']),
            "province_id": str(item['province_id']),
            "public_ip": str(item['public_ip']),
            "url": str(item['url']),
            "file_type": str("m3u8")
        }
