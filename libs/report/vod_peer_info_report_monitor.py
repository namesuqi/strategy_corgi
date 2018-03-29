#!/usr/bin/python
# coding=utf-8
# Vod Peer_info report monitor

from libs.report.report_monitor import *


class VodPeerInfoReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(VodPeerInfoReportMonitor, self).__init__()
        self.topic = TOPIC_PEER_INFO
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": "vod_peer_info",
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
            # "macs":string/null ,
            # "country":string/null,
            #  "city_id":string/null,
            # "device_info":string/null,
            # "ssid":string/null,
            # "net_change":Boolean/null ,
            "stun_ip": str(item['stun_ip'])
        }
