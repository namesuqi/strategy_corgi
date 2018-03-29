#!/usr/bin/python
# coding=utf-8
# author: Su Qi
# read push_strategy_log from push_strategy and write to logs for ELK analysis

import paramiko
from libs.common.path import *
from libs.kibana_show_log.kibana_analyse_log import path_exists
import time
import re
import json

hostname = "192.168.1.188"
port = 22
username = "root"
password = "root"


def read_push_strategy_log():
    # connection linux machine
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password, compress=True)
    sftp_client = client.open_sftp()
    # linux file path
    remote_file = sftp_client.open("/root/go_vodpush/vod-push.log")

    path_exists(LOGS_PATH)
    push_strategy_log = LOGS_PATH + "/push_strategy.log"
    fil = open(push_strategy_log, "w")

    while True:
        try:
            for line in remote_file:
                if "[INFO]" in line:
                    if "Send" in line:
                        line_time = "{year}-{month}-{day} {time}:{minute}:{second}".format(year=line[0:4],
                                                                                           month=line[5:7],
                                                                                           day=line[8:10],
                                                                                           time=line[11:13],
                                                                                           minute=line[14:16],
                                                                                           second=line[17:19])
                        # 转换成时间数组
                        time_array = time.strptime(line_time, "%Y-%m-%d %H:%M:%S")
                        # 转换成时间戳
                        timestamp = long(time.mktime(time_array) * 1000)

                        if "SDK Delete Task Count" in line:
                            # 提取line中所有数字
                            sdk_delete_line_all_number = re.sub("\D", "", line)
                            # 将需要的count过滤出来
                            sdk_delete_task_count = long(sdk_delete_line_all_number[17:][:-1])  # 去掉字符
                            if sdk_delete_task_count > 0:
                                print "sdk_delete_task_count: {0}".format(sdk_delete_task_count)
                                sdk_delete_count_combine = {
                                    "timestamp": timestamp,
                                    "sdk_delete_task_count": sdk_delete_task_count
                                }
                                sdk_delete_count_json = json.dumps(sdk_delete_count_combine)
                                fil.write(sdk_delete_count_json + "\n")
                            fil.flush()

                        if "SDK Download Task Count" in line:
                            sdk_download_line_all_number = re.sub("\D", "", line)
                            sdk_download_task_count = long(sdk_download_line_all_number[17:][:-1])
                            if sdk_download_task_count > 0:
                                print "sdk_download_task_count: {0}".format(sdk_download_task_count)
                                sdk_download_count_combine = {
                                    "timestamp": timestamp,
                                    "sdk_download_task_count": sdk_download_task_count
                                }
                                sdk_download_count_json = json.dumps(sdk_download_count_combine)
                                fil.write(sdk_download_count_json + "\n")
                            fil.flush()

                        if "Server Delete Task Count" in line:
                            push_delete_line_all_number = re.sub("\D", "", line)
                            push_delete_task_count = long(push_delete_line_all_number[17:][:-1])
                            if push_delete_task_count > 0:
                                print "push_delete_task_count: {0}".format(push_delete_task_count)
                                push_delete_count_combine = {
                                    "timestamp": timestamp,
                                    "push_delete_task_count": push_delete_task_count
                                }
                                push_delete_count_json = json.dumps(push_delete_count_combine)
                                fil.write(push_delete_count_json + "\n")
                            fil.flush()

                        if "Server Prefetch Task Count" in line:
                            push_prefetch_line_all_number = re.sub("\D", "", line)
                            push_prefetch_task_count = long(push_prefetch_line_all_number[17:][:-1])
                            if push_prefetch_task_count > 0:
                                print "push_prefetch_task_count: {0}".format(push_prefetch_task_count)
                                push_prefetch_count_combine = {
                                    "timestamp": timestamp,
                                    "push_prefetch_task_count": push_prefetch_task_count
                                }
                                push_prefetch_count_json = json.dumps(push_prefetch_count_combine)
                                fil.write(push_prefetch_count_json + "\n")
                            fil.flush()
        except Exception as e:
            print e.message

if __name__ == '__main__':
    read_push_strategy_log()
