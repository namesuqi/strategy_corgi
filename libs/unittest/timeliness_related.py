#!/usr/bin/python
# coding=utf-8
# 策略及时性相关接口开发
# author: Su Qi

import paramiko
import time


# 检查策略启动时间
def check_strategy_initialize_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.188", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    strategy_remote_file = strategy_sftp_client.open("/root/go_vodpush/vod-push.log")
    for line in strategy_remote_file:
        if "[The push strategy will begin after" in line:
            start_time = "{year}-{month}-{day} {hour}:{minute}:{second}".format(year=line[0:4], month=line[5:7],
                                                                                day=line[8:10], hour=line[11:13],
                                                                                minute=line[14:16], second=line[17:19])
            start_timestamp = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            strategy_initialize_timestamp = long(time.mktime(start_timestamp) * 1000)
            return strategy_initialize_timestamp


# 计算策略计算应开始的时间
def expect_strategy_start_calculate_time():
    # connection linux machine
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.188", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_remote_file = strategy_sftp_client.open("/root/go_vodpush/vod-push.log")
    for line in strategy_remote_file:
        if "[The push strategy will begin after" in line:
            str_line = line.encode('unicode-escape').decode('string_escape')
            time_hour = long(str_line[11:13])
            time_minute = long(str_line[14:16])
            if 9 < (time_minute + 1) < 60:
                start_time_minute = time_minute + 2
                start_time = "{year}-{month}-{day} {hour}:{minute}:00".format(year=str_line[0:4], month=str_line[5:7],
                                                                              day=str_line[8:10], hour=time_hour,
                                                                              minute=start_time_minute)
                start_timestamp = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                expect_strategy_start_time = long(time.mktime(start_timestamp) * 1000)
                return expect_strategy_start_time
            elif 0 < (time_minute + 1) <= 9:
                start_time_minute = time_minute + 2
                start_time = "{year}-{month}-{day} {hour}:{minute}:00".format(year=str_line[0:4], month=str_line[5:7],
                                                                              day=str_line[8:10], hour=time_hour,
                                                                              minute=start_time_minute)
                start_timestamp = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                expect_strategy_start_time = long(time.mktime(start_timestamp) * 1000)
                return expect_strategy_start_time
            else:
                start_time_hour = time_hour + 2
                start_time_minute = long(00)
                start_time = "{year}-{month}-{day} {hour}:{minute}:00".format(year=str_line[0:4], month=str_line[5:7],
                                                                              day=str_line[8:10], hour=start_time_hour,
                                                                              minute=start_time_minute)
                start_timestamp = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                expect_strategy_start_time = long(time.mktime(start_timestamp) * 1000)
                return expect_strategy_start_time


# 检查实际策略计算开始时间
def check_strategy_start_calculate_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.188", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_remote_file = strategy_sftp_client.open("/root/go_vodpush/vod-push.log")
    for line in strategy_remote_file:
        if "[Round:  1 starts" in line:
            real_strategy_start_time = "{year}-{month}-{day} {hour}:{minute}:{second}".format(year=line[0:4],
                                                                                              month=line[5:7],
                                                                                              day=line[8:10],
                                                                                              hour=line[11:13],
                                                                                              minute=line[14:16],
                                                                                              second=line[17:19])
            start_timestamp = time.strptime(real_strategy_start_time, "%Y-%m-%d %H:%M:%S")
            real_strategy_start_timestamp = long(time.mktime(start_timestamp) * 1000)
            return real_strategy_start_timestamp


# 检查策略预取任务下发的时间
def check_strategy_push_prefetch_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.190", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_prefetch_file = strategy_sftp_client.open("/root/corgi/logs/task_vod_push_prefetch.log")
    lines = strategy_prefetch_file.readlines()
    first_line = lines[0]
    str_line = first_line.encode('unicode-escape').decode('string_escape')
    prefetch_time = long(str_line.split(",", 5)[3].split(":")[1].split(" ")[1])
    return prefetch_time


# 检查策略sdk_download任务下发的时间
def check_strategy_sdk_download_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.190", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_download_file = strategy_sftp_client.open("/root/corgi/logs/task_vod_sdk_download.log")
    lines = strategy_download_file.readlines()
    first_line = lines[0]
    str_line = first_line.encode('unicode-escape').decode('string_escape')
    download_time = long(str_line.split(",", 6)[4].split(":")[1].split(" ")[1])
    return download_time


# 检查策略最后一次下发sdk_downlaod任务的时间
def check_strategy_sdk_download_final_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.190", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_download_file = strategy_sftp_client.open("/root/corgi/logs/task_vod_sdk_download.log")
    lines = strategy_download_file.readlines()
    last_line = lines[-1]
    str_line = last_line.encode('unicode-escape').decode('string_escape')
    last_download_time = long(str_line.split(",", 6)[4].split(":")[1].split(" ")[1])
    return last_download_time


# 检查策略push_delete任务下发的时间
def check_strategy_push_delete_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.190", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_download_file = strategy_sftp_client.open("/root/corgi/logs/task_vod_push_delete.log")
    lines = strategy_download_file.readlines()
    first_line = lines[0]
    str_line = first_line.encode('unicode-escape').decode('string_escape')
    push_delete_time = long(str_line.split(",", 5)[0].split(":")[1].split(" ")[1])
    return push_delete_time


# 检查策略sdk_delete任务下发的时间
def check_strategy_sdk_delete_time():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.190", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_download_file = strategy_sftp_client.open("/root/corgi/logs/task_vod_sdk_delete.log")
    lines = strategy_download_file.readlines()
    first_line = lines[0]
    str_line = first_line.encode('unicode-escape').decode('string_escape')
    sdk_delete_time = long(str_line.split(",", 5)[1].split(":")[1].split(" ")[1])
    return sdk_delete_time

if __name__ == "__main__":
    # expect_strategy_start_time = expect_strategy_start_calculate_time()
    # real_strategy_start_time = check_strategy_start_calculate_time()
    # print expect_strategy_start_time, real_strategy_start_time
    # time = check_strategy_sdk_download_time()
    # print time
    check_strategy_sdk_delete_time()