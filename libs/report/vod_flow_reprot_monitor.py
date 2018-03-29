#!/usr/bin/python
# coding=utf-8
# Vod_sdk_flow report monitor

from libs.report.report_monitor import *


class VodFlowReportMonitor(ReportMonitor):
    def __init__(self, log):
        super(VodFlowReportMonitor, self).__init__()
        self.topic = TOPIC_FLOW
        self.write_num = FILE_STATUS_WRITE_NUMBER
        self.log = log

    def create_topic_data(self, item):
        return {
            "topic": str("sdk_flow"),
            "timestamp": long(item['timestamp']),
            "peer_id": str(item['peer_id']),
            "play_type": str(item['play_type']),
            "file_id": str(item['file_id']),
            "duration": long(item['duration']),
            "p2p_download": long(item['p2p_download']),
            "cdn_download": long(item['cdn_download']),
            "seeds_download": long(item['seeds_download']),
            "seeds_upload": long(item['seeds_upload']),
            "public_ip": str(item['public_ip']),
            "province_id": str(item['province_id']),
            "isp_id": str(item['isp_id']),
            "operation": str(item['operation']),
            "error_type": str(item['error_type'])
        }
