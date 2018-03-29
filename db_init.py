#!/usr/bin/python
# coding=utf-8
# initialize tables according to inits
# init -> online, push_num; live_online, live_push_num
# __author__ = JinYiFan

from libs.module.inits import *
from libs.module.onlines import *
from libs.module.seed_pool import *
from libs.module.vod_push import *
from libs.module.vod_push_file import *
from libs.const.config import *
from libs.sdk.ip import get_random_private_ip, get_random_public_ip
from libs.sdk.version import *
from libs.sdk.port import *
from libs.sdk.nattype import *
from libs.sdk.peer_id import *
from libs.sdk.province_id import *
from libs.sdk.isp_id import *
from libs.database.mysql_mysqldb import *
from libs.sdk.others import *
from libs.module.live_onlines import *
from libs.module.live_peers import *
from libs.module.live_push import *
from libs.module.live_seeds import *
from libs.module.live_files import *
from libs.live_push.host_id import *
from libs.live_push.ip import *
from libs.live_push.others import *
import datetime
import sys


# --------vod tables init
# write online table
def write_online_table(online_num):
    online_list = list()
    conn = connect_mysql()
    cur = conn.cursor()
    for num in range(online_num):
        peer_id = peer_id_online_list[num]
        port = get_random_port()
        online_info = (peer_id, get_random_version(), get_random_public_ip(), port, get_random_private_ip(), port,
                       get_random_nat_type(), STUN_IP, random_isp_id(), random_province_id(), LSM_FREE, LSM_TOTAL,
                       DISK_FREE, DISK_TOTAL)
        online_list.append(online_info)

    sql = 'INSERT INTO online (peer_id, sdk_version, public_ip, public_port, private_ip, private_port, nat_type, ' \
          'stun_ip, isp_id, province_id, lsm_free, lsm_total, disk_free, disk_total) VALUES(%s, %s, %s, %s,' \
          ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cur.executemany(sql, online_list)
    cur.close()
    conn.commit()
    conn.close()
    print("write online table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# write vod_push table
def write_push_table(push_num):
    for i in range(push_num):
        vod_push = Vod_Push(push_id=PUSH_ID[i], push_ip=PUSH_IP[i], disk_size=DISK_SIZE, lsm_used=PUSH_LSM_USED[i],
                            lsm_free=PUSH_LSM_FREE[i])
        orm.session.add(vod_push)
    orm.session.commit()
    orm.session.close()
    print("write vod_push table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# --------live tables init
# write live_online table
def write_live_online_table(live_online_num):
    for i in range(live_online_num):
        peer_id = live_peer_id_online_list[i]
        port = get_random_port()
        live_online = Live_Online(peer_id=peer_id, sdk_version=get_random_version(), nat_type=get_random_nat_type(),
                                  private_ip=get_random_private_ip(), private_port=port,
                                  public_ip=get_random_public_ip(), public_port=port, province_id=random_province_id(),
                                  country=country, city_id=city_id, ssid=create_ssid(), isp_id=random_isp_id(),
                                  cppc=cppc)
        orm.session.add(live_online)
    orm.session.commit()
    orm.session.close()
    print("write live_online table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# write live_push table
def write_live_push_table(live_push_num):
    for i in range(live_push_num):
        if i < 2:
            live_push = Live_Push(host_id=get_random_host_id(), ip=create_ip(), name=name,
                                  livepush_version=livepush_version, receive=receive, transmit=transmit,
                                  bandwidth=bandwidth, cpu_count=cpu_count, cpu_load_1m=cpu_load_1m,
                                  puff_thread_count=puff_thread_count, supp_thread_count=supp_thread_count,
                                  livepush_cpu_used_percentage=livepush_cpu_used_percentage, mem_total=mem_total,
                                  mem_used=mem_used, livepush_mem_used_percentage=livepush_mem_used_percentage,
                                  event=random.choice(event_normal), reason=random.choice(reason_normal))
            orm.session.add(live_push)
        else:
            live_push = Live_Push(host_id=get_random_host_id(), ip=create_ip(), name=name,
                                  livepush_version=livepush_version, receive=receive, transmit=transmit,
                                  bandwidth=bandwidth, cpu_count=cpu_count, cpu_load_1m=cpu_load_1m,
                                  puff_thread_count=puff_thread_count, supp_thread_count=supp_thread_count,
                                  livepush_cpu_used_percentage=livepush_cpu_used_percentage, mem_total=mem_total,
                                  mem_used=mem_used, livepush_mem_used_percentage=livepush_mem_used_percentage,
                                  event=random.choice(event_unnormal), reason=random.choice(reason_unnormal))
            orm.session.add(live_push)
    orm.session.commit()
    orm.session.close()
    print("write live_push table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    print "sys.argv is", sys.argv
    print sys.argv[1]

    # read mysql
    orm = MysqlORM()

    online_num = 0
    push_num = 0
    live_online_num = 0
    live_push_num = 0

    ################################################################################
    # if init.num=1,read push_num.num and online.num, then set init.num = 0
    init = orm.session.query(Inits).filter(Inits.role == "init").one()
    if init.num == 1:
        print("need to reset data tables, start ...")
        results = orm.session.query(Inits).all()
        for result in results:
            if result.role == "online":
                online_num = int(result.num)
            elif result.role == "push_num":
                push_num = int(result.num)
            elif result.role == "live_online":
                live_online_num = int(result.num)
            elif result.role == "live_push_num":
                live_push_num = int(result.num)
        orm.session.close()

        # set init to 0
        orm.session.query(Inits).filter(Inits.role == "init").update({"num": 0})
        orm.session.commit()
        orm.session.close()

        ################################################################################
        # run vod_db_init or live_db_init according to input

        if sys.argv[1] == "vod":
            # create peer_id
            peer_id_online_list = create_peer_id(online_num)

            # clear all tables
            tables = [Online, File, Peer, Seed, Seed_pool, Vod_Push, Vod_Push_File]
            for table in tables:
                orm.session.query(table).delete()
                orm.session.commit()
            orm.session.close()

            # write datas into tables
            print "start to write datas into vod tables", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            write_online_table(online_num)
            write_push_table(push_num)
            print("write all tables done")

        if sys.argv[1] == "live":
            # create live_peer_id
            live_peer_id_online_list = create_peer_id(live_online_num)

            # clear all live_tables
            live_tables = [Live_Online, Live_Push, Live_Peer, Live_Seed, Live_File]
            for table in live_tables:
                orm.session.query(table).delete()
                orm.session.commit()
            orm.session.close()

            # write datas into tables
            print "start to write datas into live tables", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            write_live_online_table(live_online_num)
            write_live_push_table(live_push_num)
            print("write all tables done")

    else:
        print("no need to reset data tables, end")
