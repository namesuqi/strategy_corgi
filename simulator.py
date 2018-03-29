#!/usr/bin/python
# coding=utf-8
# __author__ = JinYiFan

from libs.common.log import *
from libs.common.path import *
from libs.simulator.vod_peer_info_topic_simulator import *
from libs.simulator.vod_heartbeat_topic_simulator import *
from libs.simulator.vod_peer_flow_topic_simulator import *
from libs.simulator.vod_fod_report_topic_simulator import *
from libs.simulator.vod_all_files_topic_simulator import *
from libs.simulator.vod_sdk_file_status_topic_simulator import *
from libs.simulator.vod_sdk_lsm_topic_simulator import *
from libs.simulator.vod_seed_flow_topic_simulator import *
from libs.simulator.vod_push_disk_cache_topic_simulator import *
from libs.simulator.vod_push_lsm_topic_simulator import *
from libs.simulator.vod_push_prefetch_task_topic_simulator import *
from multiprocessing import Process
from libs.simulator.live_heartbeat_topic_simulator import *
from libs.simulator.live_peer_info_topic_simulator import *
from libs.simulator.live_report_topic_simulator import *
from libs.simulator.lf_report_topic_simulator import *
import threading
import sys

start_thread_interval = 2
mutex = threading.Lock()


def ret_mutex():
    global mutex
    return mutex


if __name__ == "__main__":
    # log = Log("simulator", MONITOR_PATH + "/simulator.log")
    reviews = []
    print sys.argv[1]

    if sys.argv[1] == "vod":
        peer_info_simulator_log = Log("peer_info_log", SIMULATOR_PATH + "/peer_info.log")
        heartbeat_simulator_log = Log("heartbeat_log", SIMULATOR_PATH + "/heartbeat.log")
        fod_report_simulator_log = Log("fod_report_log", SIMULATOR_PATH + "/fod_report.log")
        all_files_simulator_log = Log("all_files_log", SIMULATOR_PATH + "/all_files.log")
        file_status_simulator_log = Log("file_status_log", SIMULATOR_PATH + "/file_status.log")
        sdk_lsm_simulator_log = Log("sdk_lsm_log", SIMULATOR_PATH + "/sdk_lsm.log")
        seed_flow_simulator_log = Log("seed_flow_log", SIMULATOR_PATH + "/seed_flow.log")
        push_disk_cache_simulator_log = Log("push_disk_cache_log", SIMULATOR_PATH + "/push_disk_cache.log")
        push_lsm_simulator_log = Log("push_lsm_log", SIMULATOR_PATH + "/push_lsm.log")
        push_prefetch_simulator_log = Log("push_prefetch_log", SIMULATOR_PATH + "/push_prefetch.log")
        peer_flow_simulator_log = Log("peer_flow_log", SIMULATOR_PATH + "/peer_flow.log")

        # start after log_generator.py
        time.sleep(10)

        # 请勿调整列表顺序，为了避免PeerInfo, HeartBeat, SDKLsm同时查询
        reviews = [
            VodPeerInfoTopicSimulator(peer_info_simulator_log),
            VodPushPrefetchTaskTopicSimulator(push_prefetch_simulator_log),
            VodFodReportTopicSimulator(fod_report_simulator_log),
            VodHeartbeatTopicSimulator(heartbeat_simulator_log),
            VodAllFilesTopicSimulator(all_files_simulator_log),
            VodSDKFileStatusTopicSimulator(file_status_simulator_log),
            VodSDKLsmTopicSimulator(sdk_lsm_simulator_log),
            VodSeedFlowTopicSimulator(seed_flow_simulator_log),
            VodPushDiskCacheTopicSimulator(push_disk_cache_simulator_log),
            VodPushLsmTopicSimulator(push_lsm_simulator_log),
            VodPeerFlowTopicSimulator(peer_flow_simulator_log)
        ]

    if sys.argv[1] == "live":
        live_peer_info_simulator_log = Log("live_peer_info_log", SIMULATOR_PATH + "/live_peer_info.log")
        live_heartbeat_simulator_log = Log("live_heartbeat_log", SIMULATOR_PATH + "/live_heartbeat.log")
        live_report_simulator_log = Log("live_report_log", SIMULATOR_PATH + "/live_report.log")
        lf_report_simulator_log = Log("lf_report_log", SIMULATOR_PATH + "/lf_report.log")
        # start after log_generator.py
        time.sleep(10)

        # 请勿调整列表顺序，为了避免PeerInfo, HeartBeat同时查询
        reviews = [LivePeerInfoTopicSimulator(live_peer_info_simulator_log),
                   LiveHeartbeatTopicSimulator(live_heartbeat_simulator_log),
                   LiveReportTopicSimulator(live_report_simulator_log),
                   LiveLFReportTopicSimulator(lf_report_simulator_log)]

    for review in reviews:
        p = Process(target=review.run, args=())
        p.daemon = True
        p.start()
        time.sleep(3)
    time.sleep(60 * 60 * 24 * 31)
