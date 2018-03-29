#!/usr/bin/python
# coding=utf-8
# Vod_sdk_lsm report monitor

from libs.report.report_monitor import *


class VodLsmReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(VodLsmReportMonitor, self).__init__()
        self.topic = TOPIC_VOD_LSM
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("vod_sdk_lsm"),
            "timestamp": long(item['timestamp']),
            "peer_id": str(item['peer_id']),
            "disk_total": long(item['disk_total']),
            "disk_free": long(item['disk_total']),
            "lsm_total": long(item['lsm_total']),
            "lsm_free": long(item['lsm_free'])
        }
