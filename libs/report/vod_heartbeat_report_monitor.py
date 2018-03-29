#!/usr/bin/python
# coding=utf-8
# Vod Heartbeat report monitor

from libs.report.report_monitor import *


class VodHeartbeatReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(VodHeartbeatReportMonitor, self).__init__()
        self.topic = TOPIC_HEARTBEAT
        self.write_num = SDK_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("vod_heartbeat"),
            "peer_id": str(item['peer_id']),
            "timestamp": long(item['timestamp']),
            "sdk_version": str(item['sdk_version']),
            "nat_type": int(item['nat_type']),
            "public_ip": str(item['public_ip']),
            "public_port": int(item['public_port']),
            "private_ip": str(item['private_ip']),
            "private_port": int(item['private_port']),
            "isp_id": str(item['isp_id']),
            "province_id": str(item['province_id']),
            # "country":string/null,
            # "city_id":string/null,
            # "ssid":string/null,
            "stun_ip": str(item['stun_ip'])
        }
