#!/usr/bin/python
# coding=utf-8
# author: Su Qi, JinYiFan

from libs.module.files import *
from libs.module.seeds import *
from testsuite.strategy_algorithm.paramiko_connect import *
import time

orm = MysqlORM()

remote_prefetch_file_dir = "/root/corgi/logs/strategy_test_task_vod_push_prefetch.log"
remote_download_file_dir = "/root/corgi/logs/strategy_test_task_vod_sdk_download.log"
remote_push_delete_file_dir = "/root/corgi/logs/strategy_test_task_vod_push_delete.log"
remote_sdk_delete_file_dir = "/root/corgi/logs/strategy_test_task_vod_sdk_delete.log"
# remote_prefetch_file_dir = "/root/corgi/logs/task_vod_push_prefetch.log"
# remote_download_file_dir = "/root/corgi/logs/task_vod_sdk_download.log"
# remote_push_delete_file_dir = "/root/corgi/logs/task_vod_push_delete.log"
# remote_sdk_delete_file_dir = "/root/corgi/logs/task_vod_sdk_delete.log"
monitor_strategy_file_dir = "/root/corgi/logs/push_strategy.log"


def check_mysql_file_num():
    """
    检查mysql file表中文件总数（dir-srv注册的文件数）
    :return: mysql file表中文件总数
    """
    mysql_file_count = orm.session.query(func.count(File.file_id)).scalar()
    orm.session.close()
    return mysql_file_count


def check_push_prefetch_task(file_id):
    """
    检查策略下发file_id对应文件的push_prefetch任务
    :return: 策略下发了该文件的预取任务，则返回True
    """
    ret = False
    # connect ftp
    sftp_client = sftp_connect()
    remote_prefetch_file = sftp_client.open(remote_prefetch_file_dir)
    lines = remote_prefetch_file.readlines()
    for line in lines:
        # print line
        str_line = line.encode('unicode-escape').decode('string_escape')
        line_file_id = str_line.split(",", 10)[8].split(": ")[1].split('"')[1]
        if line_file_id == file_id:
            ret = True
            break
    sftp_client.close()
    return ret


def check_sdk_download_task(file_id):
    """
    检查策略下发file_id对应文件的sdk_download任务
    :return: 策略下发了该文件的下载任务，则返回True
    """
    ret = False
    sftp_client = sftp_connect()
    remote_download_file = sftp_client.open(remote_download_file_dir)
    lines = remote_download_file.readlines()
    for line in lines:
        str_line = line.encode('unicode-escape').decode('string_escape')
        line_file_id = str_line.split(",", 11)[9].split(":")[1].split('"')[1]
        if line_file_id == file_id:
            ret = True
            break
    sftp_client.close()
    return ret


def check_push_delete_task(file_id):
    """
    检查策略下发file_id对应文件的push_delete任务
    :return: 策略下发了该文件的push删除任务，则返回True
    """
    ret = False
    sftp_client = sftp_connect()
    remote_push_delete_file = sftp_client.open(remote_push_delete_file_dir)
    lines = remote_push_delete_file.readlines()
    for line in lines:
        str_line = line.encode('unicode-escape').decode('string_escape')
        line_file_id = str_line.split(",", 6)[3].split(":")[1].split('"')[1]
        if line_file_id == file_id:
            ret = True
            break
    sftp_client.close()
    return ret


def check_sdk_delete_task(file_id):
    """
    检查策略下发file_id对应文件的sdk_delete任务
    :return: 策略下发了该文件的sdk删除任务，则返回True
    """
    ret = False
    sftp_client = sftp_connect()
    remote_sdk_delete_file = sftp_client.open(remote_sdk_delete_file_dir)
    lines = remote_sdk_delete_file.readlines()
    for line in lines:
        str_line = line.encode('unicode-escape').decode('string_escape')
        line_file_id = str_line.split(",", 7)[3].split(":")[1].split('"')[1]
        if line_file_id == file_id:
            ret = True
            break
    sftp_client.close()
    return ret


def check_push_prefetch_task_num():
    """
    监控task_vod_push_prefetch.log,检查策略下发的push_prefetch任务文件总数
    :return: 策略下发的push_prefetch任务总数
    """
    sftp_client = sftp_connect()
    remote_prefetch_file = sftp_client.open(remote_prefetch_file_dir)
    lines = remote_prefetch_file.readlines()
    push_prefetch_count = len(lines)
    sftp_client.close()
    return push_prefetch_count


def check_sdk_download_task_num():
    """
    监控task_vod_sdk_download.log,检查策略下发的sdk_download任务总数
    :return: 策略下发的sdk_download任务总数
    """
    sftp_client = sftp_connect()
    remote_download_file = sftp_client.open(remote_download_file_dir)
    lines = remote_download_file.readlines()
    sdk_download_count = len(lines)
    sftp_client.close()
    return sdk_download_count


def check_sdk_download_task_file_num():
    """
    监控task_vod_sdk_download.log,检查策略下发的sdk_download任务文件总数
    :return: 策略下发的sdk_download任务文件总数
    """
    sftp_client = sftp_connect()
    remote_download_file = sftp_client.open(remote_download_file_dir)
    file_id_list = list()
    lines = remote_download_file.readlines()
    for line in lines:
        str_line = line.encode('unicode-escape').decode('string_escape')
        file_id = str_line.split(",", 11)[9].split(":")[1].split('"')[1]
        if file_id not in file_id_list:
            file_id_list.append(file_id)
    print file_id_list
    sdk_download_task_file_num = len(file_id_list)
    sftp_client.close()
    return sdk_download_task_file_num


def check_strategy_download_parallel_num():
    """
    检查策略下发的sdk_download_task数目
    :return: 如果策略下发的sdk_download_task数目大于74，则返回下发的任务数；否则返回None
    """
    sftp_client = sftp_connect()
    monitor_strategy_file = sftp_client.open(monitor_strategy_file_dir)
    for line in monitor_strategy_file:
        if "sdk_download_task_count" in line:
            download_parallel_count = long(line[56:][:-2])
            if download_parallel_count > 74:
                sftp_client.close()
                return download_parallel_count


def check_strategy_prefetch_parallel_num():
    """
    检查策略下发的push_prefetch_task数目
    :return: 如果策略下发的sdk_download_task数目大于2，则返回下发的任务数；否则返回None
    """
    sftp_client = sftp_connect()
    monitor_strategy_file = sftp_client.open(monitor_strategy_file_dir)
    for line in monitor_strategy_file:
        if "push_prefetch_task_count" in line:
            prefetch_parallel_count = long(line[56:][:-2])
            if prefetch_parallel_count > 2:
                sftp_client.close()
                return prefetch_parallel_count


def check_push_prefetch_task_repeat(file_id):
    """
    检查策略是否重复下发file_id对应文件的push_prefetch任务
    :return: 策略重复下发了该文件的预取任务，则返回True
    """
    ret = False
    sftp_client = sftp_connect()
    remote_prefetch_file = sftp_client.open(remote_prefetch_file_dir)
    lines = remote_prefetch_file.readlines()
    num = 0
    for line in lines:
        # print line
        str_line = line.encode('unicode-escape').decode('string_escape')
        line_file_id = str_line.split(",", 10)[8].split(": ")[1].split('"')[1]
        if line_file_id == file_id:
            num += 1
    # print num
    if num > 1:
        ret = True
    sftp_client.close()
    return ret


def check_files_and_seed_done(ppc, last_time, file_ids):
    """
    检查单个文件下发的seed任务总数
    :param ppc: 文件的ppc
    :param last_time: 测试持续的时间
    :param file_id: 文件的file_id
    :return: 超出策略当前应下发的seed数目的文件下载完成的seed数
    """
    strategy_expect_download_seed_number = strategy_download_seed_num(ppc, last_time)
    print strategy_expect_download_seed_number
    seed_done_list = list()
    for file in file_ids:
        seed_done = orm.session.query(func.count('*')).filter(Seed.file_id == file,
                                                              Seed.file_status == "done").scalar()
        print "file:{0}, seed_done_num is {1}".format(file, int(seed_done))
        seed_done_list.append(int(seed_done))
    # print seed_done_list
    if max(seed_done_list) >= strategy_expect_download_seed_number:
        return max(seed_done_list)


def check_file_seed_download_num(file_ids):
    """
    检查单个文件下发的seed任务总数
    :param file_ids: 文件的file_id
    :return: 每个文件下发的seed数
    """
    file_count_list = list()
    sftp_client = sftp_connect()
    remote_download_file = sftp_client.open(remote_download_file_dir)
    lines = remote_download_file.readlines()
    for file_id in file_ids:
        file_count = 0
        for line in lines:
            str_line = line.encode('unicode-escape').decode('string_escape')
            line_file_id = str_line.split(",", 11)[9].split(":")[1].split('"')[1]
            if line_file_id == file_id:
                file_count += 1
        file_count_list.append(file_count)
    # print file_count_list
    sftp_client.close()
    return file_count_list


def strategy_download_seed_num(ppc, last_time):
    """
    在测试时间段内策略应下发单个文件的seed数目
    :param ppc: 文件的ppc大小
    :param last_time: 测试持续的时间(h)
    :return: 策略应下发单个文件的seed数目
    """
    now_hour = int(time.strftime('%H', time.localtime(time.time())))
    expect_hour = int(now_hour) + int(last_time)
    expect_seed_num = max(seed_number(ppc, now_hour), seed_number(ppc, expect_hour))
    return expect_seed_num


def seed_number(ppc, time):
    seed_num_base = 45 * (int(ppc) / 16)
    seed_num = 0
    if 0 <= time < 2:
        seed_num = seed_num_base * 0.6
    if 2 <= time < 6:
        seed_num = seed_num_base * 0.4
    if 6 <= time < 9:
        seed_num = seed_num_base * 0.5
    if 9 <= time < 14:
        seed_num = seed_num_base * 0.8
    if 14 <= time < 18:
        seed_num = seed_num_base * 0.6
    if 18 <= time < 20:
        seed_num = seed_num_base * 0.8
    if 20 <= time < 23:
        seed_num = seed_num_base * 1
    if 23 <= time < 24:
        seed_num = seed_num_base * 0.6
    return int(seed_num)


def check_sdk_download_task_order():
    """
    检查策略下发sdk_download_task的顺序：优先文件>点播文件>文件大小（文件小优先下载）
    :return:当策略实际下发任务顺序不符合期望顺序，返回False
    """
    ret = True
    expect_file_id_order = list()
    file_id_list = list()
    hfile = orm.session.query(File)[1].file_id
    play_file = orm.session.query(File)[0].file_id
    files_order_by_size = orm.session.query(File).order_by('file_size').all()
    orm.session.close()
    for file in files_order_by_size:
        if (file.file_id != hfile) & (file.file_id != play_file):
            file_id_list.append(file.file_id)
    # print file_id_list
    expect_file_id_order.append(hfile)
    expect_file_id_order.append(play_file)
    expect_file_id_order.extend(file_id_list)
    print expect_file_id_order

    sftp_client = sftp_connect()
    remote_download_file = sftp_client.open(remote_download_file_dir)
    actual_file_id_order = list()
    lines = remote_download_file.readlines()
    for line in lines:
        str_line = line.encode('unicode-escape').decode('string_escape')
        file_id = str_line.split(",", 11)[9].split(":")[1].split('"')[1]
        if file_id not in actual_file_id_order:
            actual_file_id_order.append(file_id)
    print actual_file_id_order

    for i in range(len(actual_file_id_order)):
        if expect_file_id_order[i] != actual_file_id_order[i]:
            ret = False
    sftp_client.close()
    return ret


if __name__ == "__main__":
    # sftp_client = sftp_connect()
    # sftp_client.close()
    # print check_sdk_download_task_file_num()

    # file_id = ['8A1CA62E5EC319ECE975647C125842C7']
    # print check_file_seed_download_num(file_id)
    # print check_push_prefetch_task_repeat(file_id)
    # print check_sdk_download_task_order()
    while True:
        print time.asctime(time.localtime(time.time()))
        file_id_list = list()
        a_s = orm.session.query(File).all()
        orm.session.close()
        for a in a_s:
            file_id_list.append(a.file_id)

        print file_id_list
        print len(file_id_list)
        print check_file_seed_download_num(file_id_list)
        time.sleep(60 * 2)
