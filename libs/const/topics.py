# coding=utf-8
# topic constant

# vod topics
TOPIC_HEARTBEAT = "vod_heartbeat"
TOPIC_VOD_LSM = "vod_sdk_lsm"
TOPIC_FILE_STATUS = "vod_sdk_file_status"
TOPIC_FLOW = "vod_sdk_flow"
TOPIC_PEER_INFO = "vod_peer_info"
TOPIC_VOD_ALLFILES = "vod_all_files"
TOPIC_FOD_REPORT = "vod_fod_report"
TOPIC_PUSH_PREFETCH = "vod_push_prefetch_task"
TOPIC_PUSH_DISK = "vod_push_disk_cache"
TOPIC_PUSH_LSM = "vod_push_lsm"
TOPIC_TASK_SDK_DELETE = "task_vod_sdk_delete"
TOPIC_TASK_SDK_DOWNLOAD = "task_vod_sdk_download"
TOPIC_TASK_PUSH_DELETE = "task_vod_push_delete"
TOPIC_TASK_PUSH_PREFETCH = "task_vod_push_prefetch"


# live topics
TOPIC_LIVE_PEER_INFO = "peer_info"
TOPIC_LIVE_HEARTBEAT = "heartbeat"
TOPIC_LIVE_SDK_REPORT = "live_report"
TOPIC_LIVE_LF_REPORT = "lf_report"
TOPIC_LIVE_QOS_BUFFER = "qos_buffering_count"   # qos只做统计,不会影响任务的下发
TOPIC_LIVE_QOS_START = "qos_startup"
TOPIC_LIVE_DIRECTIONAL_TASK = "sdk_directional_task_live"  # 任务下发的topic


# live_push topics
TOPIC_PUSH_SYSTEM_OCCUPANCY_MONITOR = "system_occupancy_monitor"  # 统计live_push运行过程中，系统占用情况
TOPIC_PUSH_NETWORK_CARD_FLOW = "network_card_flow"  # 统计live_push运行过程中，系统网卡流量情况
TOPIC_PUSH_ACL = "livepush_acl"  # 统计live_push运行过程中, 系统内存、CPU和流量的占用情况