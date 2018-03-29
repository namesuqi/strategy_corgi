# calculate vod_push prefetch_task time according to bandwidth
# calculate sdk get file time
# author: myn
from libs.common.log import Log
from libs.common.path import MONITOR_PATH
from config import push_download_bandwidth, seed_download_bandwidth

# data for push prefetch
# file_size:  B   bandwidth: Mbps
push_download_bandwidth = push_download_bandwidth
seed_download_bandwidth = seed_download_bandwidth
# bandwidth_cdn_dynamic = 1024
cdn_upload_bandwidth = 1024
# bandwidth_push_down_link_dynamic = 100
time_consuming_ratio = 1.2
# data for sdk get file
push_upload_bandwidth = 300

# MB/S
disk_read_into_memory_speed = 50

# ------------------------------------------------
# One second Request (10 times *12 pieces)
# one piece = 1392B
# 10 * 12 * 1392 B = 10 * 12 * 1392  * 8 (bps)
seed_get_file_max_speed = 1336320

log = Log("strategy_executor", MONITOR_PATH + "/strategy_executor.log")


# when: disk_read_into_memory_speed >= 50
#       control the number of concurrent push service <= 100
# we can use this to calculate


# file_size: B
def sdk_get_file_time_consume(file_size, ppc):
    time_seed_add_cost = file_size * 8.0 / ppc / min(
        seed_get_file_max_speed,
        seed_download_bandwidth * 1000000,
        push_upload_bandwidth * 1000000)
    log.logger.info('seed download file will cost time: {0}s'.format(
        time_seed_add_cost))
    return time_seed_add_cost / 10.0


def push_prefetch_time_consume(file_size):
    # bandwidth = min(bandwidth_cdn, bandwidth_push_down_link)
    time_prefetch_cost = (file_size * 8.0 / min(push_download_bandwidth * 1000000,
                                                cdn_upload_bandwidth * 1000000)) * time_consuming_ratio
    print time_prefetch_cost
    return time_prefetch_cost / 10.0


if __name__ == "__main__":
    # push_prefetch_time_consume(1073741824)
    sdk_get_file_time_consume(5431561218, 272)
