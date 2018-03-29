#!/usr/bin/python
# coding=utf-8
# Live qos_buffering_count report monitor

from libs.report.report_monitor import *


class LiveQosBufferReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(LiveQosBufferReportMonitor, self).__init__()
        self.topic = TOPIC_LIVE_QOS_BUFFER
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "qos_buffering_count",
            "id": str(item['id']),
            "peer_id": str(item['peer_id']),
            "timestamp": long(item['timestamp']),
            "play_type": str(item['play_type']),
            "url": str(item['url']),
            "vvid": str(item['vvid']),
            "buffering_count": int(item['buffering_count']),
            "public_ip": str(item['public_ip']),
            "input_time": long(item['input_time']),
            "sdk_agent_time": str(item['sdk_agent_time']),
            "sdk_agent_version": str(item['sdk_agent_version'])
        }
