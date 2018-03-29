#!/usr/bin/python
# coding=utf-8
# LF策略及时性相关接口开发
# author: Su Qi

import paramiko
import time


# 获取策略开始计算时间
def check_lf_strategy_start_time():
    # connection linux machine
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.188", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_remote_file = strategy_sftp_client.open("/root/dslive/lf_strategy.out")
    cycle_list = []
    for line in strategy_remote_file:
        if "Count of peer_detail" in line:
            cycle_time = line[0:17]
            start_timestamp = time.strptime(cycle_time, "%Y%m%d-%H:%M:%S")
            real_strategy_start_timestamp = long(time.mktime(start_timestamp) * 1000)
            cycle_list.append(real_strategy_start_timestamp)
    cycle_start_time = cycle_list[0]
    return cycle_start_time


# 检查策略计算周期时间
def check_lf_strategy_compute_cycle_time():
    # connection linux machine
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.188", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_remote_file = strategy_sftp_client.open("/root/dslive/lf_strategy.outtest")
    cycle_list = []
    for line in strategy_remote_file:
        if "Count of peer_detail" in line:
            cycle_time = line[0:17]
            start_timestamp = time.strptime(cycle_time, "%Y%m%d-%H:%M:%S")
            real_strategy_start_timestamp = long(time.mktime(start_timestamp) * 1000)
            cycle_list.append(real_strategy_start_timestamp)
    cycle_time_less = cycle_list[1:]
    cycle_time_minus = list(map(lambda x: x[0] - x[1], zip(cycle_time_less, cycle_list)))
    cycle_time_list = list(set(cycle_time_minus))
    for cycle_time_only in cycle_time_list:
        return cycle_time_only


# 检查策略下发download任务的时间
def check_lf_strategy_sdk_download_start_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.217", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_download_file = strategy_sftp_client.open("/root/corgi/logs/sdk_directional_task_live.log")
    lines = strategy_download_file.readlines()
    first_line = lines[0]
    str_line = first_line.encode('unicode-escape').decode('string_escape')
    last_download_time = long(str_line.split(",", 3)[0].split(":")[1].split(" ")[1])
    return last_download_time


# 检查策略下发delete任务的时间
def check_lf_strategy_sdk_delete_start_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.217", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_download_file = strategy_sftp_client.open("/root/corgi/logs/sdk_directional_task_live.log")
    lines = strategy_download_file.readlines()
    delete_list = []
    for line in lines:
        if "delete" in line:
            last_download_time = long(line.split(",", 3)[0].split(":")[1].split(" ")[1])
            delete_list.append(last_download_time)
    delete_first_time = list(set(delete_list))[0]
    return delete_first_time

if __name__ == '__main__':
    check_lf_strategy_sdk_delete_start_time()
