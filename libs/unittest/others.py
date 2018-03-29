#!/usr/bin/python
# coding=utf-8
# author: JinYiFan

from libs.common.path import MONITOR_PATH


def file_download_all_time():
    """
    文件从开始预取到下载完成的时间
    :return: 文件文件从开始预取到下载完成的时间， seed下载完成的时间点，push_prefetch任务下发的时间点
    """
    strategy_log = MONITOR_PATH + "/{0}.log".format("strategy_executor")
    push_prefetch_get_times = []
    seed_done_times = []
    with open(strategy_log, "r") as f:
        for line in f.readlines():
            if "push prefetch task at" in line:
                push_prefetch_get_times.append(line)
            if "seed done at" in line:
                seed_done_times.append(line)

        seed_done_time = seed_done_times[-1].split("time:", 1)[-1].split("\n")[0]
        print "seed_done_time is", seed_done_time

        push_prefetch_time = push_prefetch_get_times[-1].split("time:", 2)[-1].split("\n")[0] + ""
        print "push_prefetch_time is", push_prefetch_time

    file_download_time = long(float(seed_done_time)) - long(float(push_prefetch_time))
    print "file_download_time is", file_download_time
    return file_download_time, seed_done_time, push_prefetch_time
