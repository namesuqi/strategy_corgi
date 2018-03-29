#!/usr/bin/python
# coding=utf-8
# description: mock strategy's tasks
# 1. select online SDKs which is not act as seeds
# 2. write down task to kafka download topic for strategy_executor consume
# ========= function add
# 3. If the number of seeds is less than 600, 100 pull-in tasks  per minute until more 600; if the number of
# seeds is greater than 600 100 per minute is deleted until 200
# author: myn

import time
from libs.database.handle_kafka import write_logs_to_kafka
from libs.database.mysql_orm import MysqlORM
from libs.module.onlines import Online
from libs.module.seeds import Seed

# frequency of calculate  online seed
# from libs.module.vod_push_file import Vod_Push_File
# from misc.mock_tool.obtain_file_time_mocker import sdk_get_file_time_consume

mock_data_generation_duration = 50

orm = MysqlORM()


def obtain_peer_id_from_table(table):
    """
    function:get peer id from table
    :param table: online/seed/peer
    :return:peer-id list
    """
    peer_ids = []
    results = orm.session.query(table).all()
    for result in results:
        peer_ids.append(result.peer_id)
    orm.session.close()
    return peer_ids


# select peer_id make download task(num:10)
def create_download_tasks(task_num=1):
    tasks = []
    online_sdk_list = obtain_peer_id_from_table(Online)
    online_sdk_set = set(online_sdk_list)
    seed_sdk_list = obtain_peer_id_from_table(Seed)
    seed_sdk_set = set(seed_sdk_list)
    list_online_not_seed = list(online_sdk_set ^ seed_sdk_set)
    # print list_onlie_not_seed
    for peer_id in list_online_not_seed[0:task_num]:
        # print type(peer_id)
        task_vod_sdk_download = {
            "file_id": "77BFD961FA87492A860E211E7E5600D2",
            "file_size": 775134238,
            "file_url": "http://1111111.flv",
            "ppc": 304,
            "cppc": 1,
            "piece_size": 11111,
            "priority": 10,
            "operation": 'download',
            "timestamp": long(round(time.time() * 1000)),
            "peer_id": peer_id,
            "push_ip": "192.168.1.214",
            "push_port": 80,
            "isp_id": 'zz',
            "province_id": 'zz'
        }
        tasks.append(task_vod_sdk_download)
    return tasks


def create_delete_tasks(task_num=10):
    tasks = []
    seed_sdk_list_for_del = obtain_peer_id_from_table(Seed)[0:task_num]
    for peer_id in seed_sdk_list_for_del:
        task_vod_sdk_del = {
            "file_id": "77BFD961FA87492A860E211E7E5600p2",
            "priority": 10,
            "operation": 'del',
            "timestamp": long(round(time.time() * 1000)),
            "peer_id": peer_id,
            "isp_id": 'zz',
            "province_id": 'zz'
        }
        tasks.append(task_vod_sdk_del)
    return tasks


def create_push_prefetch_tasks():
    task = [{
        "file_id": "77BFD961FA87492A860E211E7E560088",
        "file_size": 55,
        "file_url": 'test',
        "ppc": 1,
        "cppc": 1,
        "piece_size": 5555,
        "priority": 1,
        "operation": 'add',
        "timestamp": 44444444,
        "push_id": '00:16:3E:06:C3:A6',
        "push_ip": '118.190.153.230',
    }]  # {
    #     "file_id": "77BFD961FA87492A860E211E7E5600g8",
    #     "file_size": 55,
    #     "file_url": 'test',
    #     "ppc": 1,
    #     "cppc": 1,
    #     "piece_size": 5555,
    #     "priority": 1,
    #     "operation": 'add',
    #     "timestamp": 44444444,
    #     "push_id": '00:16:3E:06:C3:A6',
    #     "push_ip": '118.190.153.230',
    # }]
    # },
    #     {
    #         "file_id": "77BFD961FA87492A860E211E7E5600D3",
    #         "file_size": 555,
    #         "file_url": 'test',
    #         "ppc": 304,
    #         "cppc": 1,
    #         "piece_size": 1392,
    #         "priority": 1,
    #         "operation": 'add',
    #         "timestamp": 44444444,
    #         "push_id": '00:16:3E:06:C3:A7',
    #         "push_ip": '112.190.153.230',
    #     }]
    return task


if __name__ == '__main__':
    # info_online = orm.session.query(Online).filter_by(peer_id='00000004374EA8C21727B80AF946BC3D').first()
    # print info_online.lsm_free
    # orm = MysqlORM()
    # info_seed = orm.session.query(Seed).filter_by(
    #     peer_id='000000042EE9EA9121CD0F0B4A9FA666', file_id='A70E67C3A0A542AA9926A14798B6D1zD').first()
    # info_online = orm.session.query(Seed).filter_by(peer_id='000000042EE9EA9121CD0F0B4A9FA666',
    #                                                 file_id = 'A70E67C3A0A542AA9926A14798B6D1DD').first()
    # print info_seed
    # if info_seed is None:
    #     print 'hahah'
    # peer_ids = []
    # a = orm.session.query(Online).filter("id>9000").all()
    # for i in a:
    #     peer_ids.append(i.peer_id)
    #
    #
    # task_vod_sdk_downlods = []
    # if 0 ==1:
    #     print 's'
    # while True:
    peer_ids = []
    orm = MysqlORM()
    #
    peer_infos = orm.session.query(Online).all()
    for peer_info in peer_infos:
        peer_ids.append(peer_info.peer_id)
    print peer_ids
    print len(peer_ids)

    task_vod_sdk_downloads = []
    for peer_id in peer_ids:
        task_vod_sdk_download = {
            "file_id": "A70E67C3A0A542AA9926A14798B6D1DD",
            "file_size": 354,
            "file_url": "http://1111111.flv",
            "timestamp": 44444444,
            "ppc": 304,
            "cppc": 1,
            "piece_size": 11111,
            "priority": 10,
            "operation": 'download',
            "peer_id": peer_id,
            "push_ip": "192.168.1.214",
            "push_port": 80,
            "isp_id": 'zz',
            "province_id": 'zz'
        }
        task_vod_sdk_downloads.append(task_vod_sdk_download)
    write_logs_to_kafka(task_vod_sdk_downloads, 'task_vod_sdk_download')
# time.sleep(2)

# num = orm.session.query(Seed).filter_by(file_status='downloading').all()
# print len(num)
# download_tasks = create_push_prefetch_tasks()
# write_logs_to_kafka(download_tasks, "task_vod_push_prefetch")
# import sqlalchemy
# print sqlalchemy.__version__
# # peer_ids = []
# a = orm.session.query(Online).all()
# for x in a:
#     peer_ids.append(x.peer_id)
# print len(peer_ids)
# print '00000004D3681F33DFC05A7DB1EDADBF' in peer_ids
# info_online = orm.session.query(Seed).filter_by(
#     peer_id="00000004A3148D7B18D8FAB2A9BEAAF1").filter_by(file_id='1D38ED6BA58D4BEE942D4E51CC62A886').all()
# print info_online
# a = orm.session.query(Online).filter_by(
#     peer_id="00000004D3681F33DFC05A7DB1EDADBF").first()
# print a
# print orm.session.query(Seed).filter_by(
#     peer_id='00000004681DB5A4E50DA74A0AB4D7CB').filter_by(
#     file_id='1D38ED6BA58D4BEE942D4E51CC62A886').update(
#     {'file_status': 'done'})
# orm.session.commit()
# orm.session.close()
# info_online = orm.session.query(Online).filter_by(
#     peer_id='00000004DD7B0F00A24A365569B7289A').first()
# print info_online.version
# b= orm.session.query(Online.peer_id).all()
# a = orm.session.query(Online.peer_id).all()[0][0]
# print a
# if a in b:
#     print 'aaa'
# pid = [u'00000004DD7B0F00A24A365569B7289A']
# info_online = orm.session.query(Online).filter_by(
#     peer_id=pid[0]).first()
# print info_online.sdk_version
# a = orm.session.query(Seed).filter_by(peer_id="00000004F67A9996689F7EB9715E4CDF").first()
# if a is None:
#     print 'a'
# print info_online.sdk_version
# create_download_tasks
# tasks = create_push_prefetch_tasks()
#

# log = Log("mock_strategy_task", MONITOR_PATH+"/mock_strategy_task.log")
# time.sleep(5)
#
# while True:
#     seed_sdk_num = len(obtain_peer_id_from_table(Seed))
#     print("    seed num is: {0}".format(seed_sdk_num))
#
#     while seed_sdk_num < 600:
#         print "================================"
#         print "    if num>600, decrease num to 200"
#         # add to 600
#         log.logger.info("now seed num is: {0}".format(seed_sdk_num))
#         time_start = time.time()
#
#         log.logger.info("mock_strategy_task output add seeds task num : {100}")
#         time_cost = time.time() - time_start
#         time.sleep(60-time_cost)
#         seed_sdk_num = len(obtain_peer_id_from_table(Seed))
#         print("    seed num is: {0}".format(seed_sdk_num))
#
#     while seed_sdk_num > 200:
#         print "================================"
#         print "    if num>200, increase num to 600"
#         # reduce to 200
#         log.logger.info("seed num is: {0}".format(seed_sdk_num))
#         time_start = time.time()
#         delete_tasks = create_delete_tasks(100)
#         write_logs_to_kafka(delete_tasks, "task_vod_sdk_delete")
#         log.logger.info("mock_strategy_task output del seeds task num : {100}")
#         time_cost = time.time() - time_start
#         time.sleep(60-time_cost)
#         seed_sdk_num = len(obtain_peer_id_from_table(Seed))
#         print("now seed num is: {0}".format(seed_sdk_num))
