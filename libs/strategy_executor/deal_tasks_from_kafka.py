#!/usr/bin/python
# coding=utf-8
# execute kafka tasks and write results to mysql
# author = 'myn'

from libs.module.vod_push import *
from libs.module.onlines import *
from libs.module.seeds import *
from libs.module.vod_push_file import *
from libs.const.config import *
from libs.database.handle_kafka import *
from libs.const.topics import *
from libs.module.files import *

orm = MysqlORM()


def deal_sdk_del_tasks(task_info):
    peer_id = task_info['peer_id']
    file_id = task_info['file_id']

    # 从file表中查到此file_id对应的file_size, ppc
    sdk_del_file_id_equal = orm.session.query(File).filter_by(file_id=file_id).first()
    sdk_del_file_size = sdk_del_file_id_equal.file_size
    sdk_del_file_ppc = sdk_del_file_id_equal.ppc

    # 释放SDK的空间:查找online表,更新lsm_free
    sdk_del_info_online = orm.session.query(Online).filter_by(peer_id=peer_id).first()
    sdk_del_lsm_free = sdk_del_info_online.lsm_free + sdk_del_file_size / sdk_del_file_ppc
    orm.session.query(Online).filter_by(peer_id=peer_id).update({'lsm_free': sdk_del_lsm_free})
    orm.session.commit()
    orm.session.close()

    result = orm.session.query(Seed).filter_by(file_id=file_id, peer_id=peer_id)
    if result.first():
        result.delete()
        orm.session.commit()
        orm.session.close()


def deal_push_prefetch_tasks(task_info, file_id, push_id, file_size):
    push_ip = task_info['push_ip']
    disk_size = 0
    flag = 'downloading'
    universe = 'true'

    push_info = orm.session.query(Vod_Push).filter_by(push_id=str(push_id)).first()
    lsm_used = push_info.lsm_used + file_size
    lsm_free = push_info.lsm_free - file_size
    if lsm_free >= 0 and lsm_used >= 0:
        add_task_info = Vod_Push_File(
            file_id=file_id,
            file_size=file_size,
            flag=flag,
            push_id=push_id,
            push_ip=push_ip,
            disk_size=disk_size,
            lsm_free=lsm_free,
            lsm_used=lsm_used,
            universe=universe)

        # avoid receive repeat tasks
        orm.session.add(add_task_info)

        # change push lsm space
        orm.session.query(Vod_Push).filter_by(push_id=push_id).update({'lsm_used': lsm_used})
        orm.session.query(Vod_Push).filter_by(push_id=push_id).update({'lsm_free': lsm_free})
        orm.session.commit()
        orm.session.close()
    else:
        pass


def deal_push_del_tasks(task_info):
    file_id = task_info['file_id']
    push_id = task_info['push_id']
    # 从file表中查到此file_id对应的file_size
    file_id_equal = orm.session.query(File).filter_by(file_id=file_id).first()
    file_size = file_id_equal.file_size
    # 释放push的空间
    del_push_info = orm.session.query(Vod_Push).filter_by(push_id=str(push_id)).first()
    push_del_lsm_used = del_push_info.lsm_used - file_size
    push_del_lsm_free = del_push_info.lsm_free + file_size

    orm.session.query(Vod_Push).filter_by(push_id=push_id).update({'lsm_used': push_del_lsm_used})
    orm.session.query(Vod_Push).filter_by(push_id=push_id).update({'lsm_free': push_del_lsm_free})
    orm.session.commit()
    orm.session.close()

    aim = orm.session.query(Vod_Push_File).filter_by(file_id=file_id, push_id=push_id)
    if aim.first():
        aim.delete()
        orm.session.commit()
        orm.session.close()


def deal_sdk_download_tasks(task_info, peer_id):
    info_online = orm.session.query(Online).filter_by(peer_id=peer_id).first()
    lsm_free = info_online.lsm_free - task_info['file_size'] / task_info['ppc']
    if lsm_free >= 0:
        add_task_info = Seed(
            file_status='downloading',
            file_id=task_info['file_id'],
            file_size=task_info['file_size'],
            file_url=task_info['file_url'],
            ppc=task_info['ppc'],
            cppc=task_info['cppc'],
            piece_size=task_info['piece_size'],
            priority=task_info['priority'],
            operation=task_info['operation'],
            peer_id=task_info['peer_id'],
            push_ip=task_info['push_ip'],
            push_port=task_info['push_port'],
            isp_id=task_info['isp_id'],
            province_id=task_info['province_id'],
            sdk_version=info_online.sdk_version,
            public_ip=info_online.public_ip,
            public_port=info_online.public_port,
            private_ip=info_online.private_ip,
            private_port=info_online.private_port,
            nat_type=info_online.nat_type,
            stun_ip=info_online.stun_ip,
            lsm_free=lsm_free,
            lsm_total=info_online.lsm_total,
            disk_total=info_online.disk_total,
            disk_free=info_online.disk_free,
            play_type=PLAY_TYPE,
            duration=DURATION,
            p2p_download=0,
            cdn_download=0,
            seeds_download=0,
            seeds_upload=0,
            error_type=ERROR_TYPE)
        orm.session.add(add_task_info)

        # change online sdk lsm_free space
        orm.session.query(Online).filter_by(peer_id=peer_id).update({'lsm_free': lsm_free})
        orm.session.commit()
        orm.session.close()
    else:
        pass


if __name__ == "__main__":
    schemas = search_schema([TOPIC_TASK_SDK_DOWNLOAD,
                             TOPIC_TASK_SDK_DELETE,
                             TOPIC_TASK_PUSH_PREFETCH,
                             TOPIC_TASK_PUSH_DELETE])
    new_consumers = new_consumer([TOPIC_TASK_SDK_DOWNLOAD,
                                  TOPIC_TASK_SDK_DELETE,
                                  TOPIC_TASK_PUSH_PREFETCH,
                                  TOPIC_TASK_PUSH_DELETE],
                                 'Kiroff_debug',
                                 KAFKA_ADDRESS)

    while True:
        received_all_tasks = read_logs_from_kafka(new_consumers, schemas)
        for task in received_all_tasks:
            # print "task is", task
            if len(task[2]) == 14:
                pass
            if len(task[2]) == 11:
                pass
            # deal_sdk_add_tasks(task)
        time.sleep(5)
