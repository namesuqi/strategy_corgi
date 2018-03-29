#!/usr/bin/python
# coding=utf-8
# author: Su Qi, JinYiFan

from testsuite.strategy_algorithm.paramiko_connect import *

remote_file_dir = "/root/corgi/logs/sdk_directional_task_live.log"


def check_sdk_download_task_num():
    """
    检查策略下发每个文件的sdk_download任务数
    :return: 返回每个文件的sdk下载任务数
    """
    result = dict()
    # connect ftp
    sftp_client = sftp_connect()
    remote_prefetch_file = sftp_client.open(remote_file_dir)
    lines = remote_prefetch_file.readlines()

    for line in lines:
        # print line
        str_line = line.encode('unicode-escape').decode('string_escape')
        line_operation = str_line.split(",", 5)[1].split(": ")[1].split('"')[1]

        if line_operation == "download":
            line_file_id = str_line.split(",", 5)[3].split(": ")[1].split('"')[1]
            if line_file_id not in result.keys():
                result[line_file_id] = 1
            else:
                result[line_file_id] += 1

    print result
    # print result.values()
    sftp_client.close()
    return result.values()


def check_sdk_delete_task_num():
    """
    检查策略下发每个文件的sdk_delete任务数
    :return: 返回每个文件的sdk删除任务数
    """
    result = dict()
    # connect ftp
    sftp_client = sftp_connect()
    remote_prefetch_file = sftp_client.open(remote_file_dir)
    lines = remote_prefetch_file.readlines()

    for line in lines:
        # print line
        str_line = line.encode('unicode-escape').decode('string_escape')
        line_operation = str_line.split(",", 5)[1].split(": ")[1].split('"')[1]

        if line_operation == "delete":
            line_file_id = str_line.split(",", 5)[3].split(": ")[1].split('"')[1]
            if line_file_id not in result.keys():
                result[line_file_id] = 1
            else:
                result[line_file_id] += 1

    print result
    # print result.values()
    sftp_client.close()
    return result.values()


if __name__ == "__main__":
    print check_sdk_download_task_num()
