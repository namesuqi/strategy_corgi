#!/usr/bin/python
# coding=utf-8
# Live qos_startup report monitor

from libs.report.report_monitor import *


class LiveQosStartupReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(LiveQosStartupReportMonitor, self).__init__()
        self.topic = TOPIC_LIVE_QOS_START
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "qos_startup",
            "id": str(item['id']),
            "peer_id": str(item['peer_id']),
            "timestamp": long(item['timestamp']),
            "play_type": str(item['play_type']),
            "url": str(item['url']),
            "vvid": str(item['vvid']),
            "public_ip": str(item['public_ip'])
            # "duration": long(item['duration'])
        }
