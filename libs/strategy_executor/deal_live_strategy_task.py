#!/usr/bin/python
# coding=utf-8
# execute live kafka tasks and write results to mysql
# author = Su Qi

from libs.module.live_onlines import *
from libs.module.live_seeds import *
import threading

orm = MysqlORM()


def delete_seed(peer_id, file_id):
    aim = orm.session.query(Live_Seed).filter_by(peer_id=peer_id, file_id=file_id)
    aim.delete()
    orm.session.commit()
    orm.session.close()
    print "------------------------delete seed"


def change_operation_to_null(peer_id, file_id):
    orm.session.query(Live_Seed).filter_by(peer_id=peer_id, file_id=file_id).update({'operation': ''})
    orm.session.commit()
    orm.session.close()
    print "---------------change operation to null"


def deal_live_strategy_tasks(task_info, peer_id, file_id):
    live_info_online = orm.session.query(Live_Online).filter_by(peer_id=peer_id).first()
    live_info_seed = orm.session.query(Live_Seed).filter_by(peer_id=peer_id, file_id=file_id).all()
    operation = task_info['operation']

    if operation == "download":
        if len(live_info_seed) == 0:
            add_task_info = Live_Seed(
                peer_id=peer_id,
                file_id=file_id,
                operation="add",
                version=live_info_online.sdk_version,
                country=live_info_online.country,
                province_id=live_info_online.province_id,
                city_id=live_info_online.city_id,
                isp_id=live_info_online.isp_id,
                cppc=live_info_online.cppc,
                ssid=live_info_online.ssid,
                # lfsid=live_info_online.lfsid,
                # uid_index=live_info_online.uid_index,
                upload=24690,
                download=12345)
            orm.session.add(add_task_info)
            orm.session.commit()
            orm.session.close()
            print "add"

            timer = threading.Timer(60, change_operation_to_null, (peer_id, file_id))
            timer.start()

    if operation == "delete":
        if len(live_info_seed) != 0:
            aim = orm.session.query(Live_Seed).filter_by(peer_id=peer_id, file_id=file_id)
            aim.update({'operation': 'del'})
            orm.session.commit()
            orm.session.close()

            timer = threading.Timer(60, delete_seed, (peer_id, file_id))
            timer.start()

            print "del"
