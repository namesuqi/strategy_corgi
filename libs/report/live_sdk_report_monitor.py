#!/usr/bin/python
# coding=utf-8
# Live live_report report monitor

from libs.report.report_monitor import *


class LiveSDKReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(LiveSDKReportMonitor, self).__init__()
        self.topic = TOPIC_LIVE_SDK_REPORT
        self.write_num = FILE_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("live_report"),
            "timestamp": long(item['timestamp']),
            "peer_id": str(item['peer_id']),
            "version": str(item['version']),
            "country": str(item['country']),
            "province_id": str(item['province_id']),
            "city_id": str(item['city_id']),
            "isp_id": str(item['isp_id']),
            "file_id": str(item['file_id']),
            "chunk_id": long(item['chunk_id']),
            "operation": str(item['operation']),
            "cdn": long(item['cdn']),
            "p2p": long(item['p2p']),
            "p2penable": item['p2penable'],
            "ssid": str(item['ssid'])
        }
