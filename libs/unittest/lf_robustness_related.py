#!/usr/bin/python
# coding=utf-8
# author: Su Qi

import paramiko
from libs.module.live_files import *
from libs.module.live_seeds import *
from libs.module.live_peers import *


def check_lf_strategy_player_count():
    """
    检查播放节点的个数
    :return: 返回播放节点的个数
    """
    orm = MysqlORM()
    mysql_play_count = orm.session.query(func.count(Live_Peer.file_id)).scalar()
    orm.session.close()
    return mysql_play_count


def check_lf_strategy_each_download_num():
    """
    检查策略每轮下发的download任务数
    :return:返回每轮下发的download任务数
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.190", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_task_file = strategy_sftp_client.open("/root/corgi/monitor/read_task_main.log")
    task_num_list = []
    for line in strategy_task_file:
        if "read_sdk_download_task_live" in line:
            task_num = long(line[62:-7])
            task_num_list.append(task_num)
    return task_num_list


def check_lf_strategy_each_delete_num():
    """
    检查策略每轮下发的delete任务数
    :return:返回每轮下发的delete任务数
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.3.190", 22, "root", "root", compress=True)
    strategy_sftp_client = client.open_sftp()
    # linux file path
    strategy_task_file = strategy_sftp_client.open("/root/corgi/monitor/read_task_main.log")
    task_num_list = []
    for line in strategy_task_file:
        if "read_sdk_delete_task_live" in line:
            task_num = line[60:-7]
            task_num_list.append(task_num)
    return task_num_list


def check_lf_seed_table_count():
    """
    检查live_seed表中雷锋节点总数
    :return:
    """
    orm = MysqlORM()
    for file in orm.session.query(Live_File).all():
        seed_done = orm.session.query(func.count('*')).filter(Live_Seed.file_id == file.file_id).scalar()
        orm.session.close()
        return seed_done

if __name__ == "__main__":
    check_lf_seed_table_count()
