#!/usr/bin/python
# coding=utf-8
# Live_push network_card_flow report monitor

from libs.report.report_monitor import *


class LivePushNetworkCardFlowMonitor(ReportMonitor):
    def __init__(self, log):
        super(LivePushNetworkCardFlowMonitor, self).__init__()
        self.topic = TOPIC_PUSH_NETWORK_CARD_FLOW
        self.write_num = PUSH_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "network_card_flow",
            "timestamp": long(item['timestamp']),
            "name": str(item['name']),
            "receive": long(item['receive']),
            "transmit": long(item['transmit']),
            "bandwidth": long(item['bandwidth']),
            "ip": str(item['ip']),
            "host_id": str(item['host_id']),
            # "detail_info": str(item['detail_info'])
        }
