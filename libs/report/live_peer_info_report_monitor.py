#!/usr/bin/python
# coding=utf-8
# Live Peer_info report monitor

from libs.report.report_monitor import *


class LivePeerInfoReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(LivePeerInfoReportMonitor, self).__init__()
        self.topic = TOPIC_LIVE_PEER_INFO
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "peer_info",
            "peer_id": str(item['peer_id']),
            "timestamp": long(item['timestamp']),
            "sdk_version": str(item['sdk_version']),
            "nat_type": int(item['nat_type']),
            "public_ip": str(item['public_ip']),
            "public_port": int(item['public_port']),
            "private_ip": str(item['private_ip']),
            "private_port": int(item['private_port']),
            "province_id": str(item['province_id']),
            "isp_id": str(item['isp_id']),
            "country": str(item['country']),
            "city_id": str(item['city_id']),
            "ssid": str(item['ssid']),
            "net_change": str(item['net_change'])
            # "macs":string/null ,
            # "device_info":string/null,
        }
