#!/usr/bin/python
# coding=utf-8
# write logs and live_logs for ELK analysis according to SDK simulator generated task list
# at the same time, write the data to kafka for strategy system
# 1. different monitor to watch different redis channel and write to different logs
# 2. only append to log instead of create a new log(TBD)
# author: Su Qi


from libs.common.log import *
from libs.report.vod_heartbeat_report_monitor import *
from libs.report.vod_peer_info_report_monitor import *
from libs.report.vod_flow_reprot_monitor import *
from libs.report.vod_lsm_report_monitor import *
from libs.report.vod_file_status_report_monitor import *
from libs.report.vod_all_files_report_monitor import *
from libs.report.vod_fodreport_report_monitor import *
from libs.report.push_lsm_report_monitor import *
from libs.report.push_disk_cache_report_monitor import *
from libs.report.push_prefetch_task_report_monitor import *
from libs.report.live_directional_task_report_monitor import *
from libs.report.live_heartbeat_report_monitor import *
from libs.report.live_lf_report_monitor import *
from libs.report.live_peer_info_report_monitor import *
from libs.report.live_sdk_report_monitor import *
from libs.report.livepush_system_occupancy_monitor import *
from multiprocessing import Process
import shutil
import sys

if __name__ == "__main__":
    print sys.argv[1]

    print "log generator get started..."
    print "remove logs dir and recreate it"
    shutil.rmtree(LOGS_PATH)
    os.mkdir(LOGS_PATH)
    monitors = []
    log = Log("log_generator.py", MONITOR_PATH + "/log_generator.log")

    if sys.argv[1] == "vod":
        monitors = [
            VodHeartbeatReportMonitor(log),
            VodPeerInfoReportMonitor(log),
            VodFlowReportMonitor(log),
            VodLsmReportMonitor(log),
            VodFileStatusReportMonitor(log),
            VodAllFilesReportMonitor(log),
            VodFodReportReportMonitor(log),
            PushLsmReportMonitor(log),
            PushDiskCacheReportMonitor(log),
            PushPrefetchTaskReportMonitor(log)
        ]

    if sys.argv[1] == "live":
        monitors = [
            LiveDirectionTaskReportMonitor(log),
            LiveHeartbeatReportMonitor(log),
            LiveLFReportMonitor(log),
            LivePeerInfoReportMonitor(log),
            LiveSDKReportMonitor(log)
        ]

    for monitor in monitors:
        p = Process(target=monitor.run, args=())
        p.daemon = True
        p.start()
    time.sleep(60 * 60 * 24 * 31)
