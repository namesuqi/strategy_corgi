#!/usr/bin/python
# coding=utf-8
# simulate sdk login and logout at random
# __author__ = JinYiFan

from libs.module.onlines import *
from libs.module.inits import *
from libs.database.mysql_orm import *
from libs.common.log import *
from libs.common.path import MONITOR_PATH
import time
import datetime

log = Log("scene", MONITOR_PATH + "/scene.log")
orm = MysqlORM()


def sdk_fluctuate(sdk_stable_online_rate):
    online_count = orm.session.query(Online).count()
    total_count = orm.session.query(Inits).filter(Inits.role == "online").one()
    sdk_change_num = int(total_count.num * (1 - sdk_stable_online_rate))
    results = orm.session.query(Online).limit(sdk_change_num).all()
    orm.session.close()

    sdk_change(results, total_count, online_count)


# need online sdk num at different hours
# 0-2:0.6,   2-6:0.4,   6-9:0.5,   9-14:0.8,   14-18:0.6,   18-20:0.8,  20-23:1,  23-24:0.6
def need_online_num(now_hour, total_count):
    if 0 <= now_hour < 2:
        need_count = int(total_count.num * 0.6)
    if 2 <= now_hour < 6:
        need_count = int(total_count.num * 0.4)
    if 6 <= now_hour < 9:
        need_count = int(total_count.num * 0.5)
    if 9 <= now_hour < 14:
        need_count = int(total_count.num * 0.8)
    if 14 <= now_hour < 18:
        need_count = int(total_count.num * 0.6)
    if 18 <= now_hour < 20:
        need_count = int(total_count.num * 0.8)
    if 20 <= now_hour < 23:
        need_count = int(total_count.num * 1)
    if 23 <= now_hour < 24:
        need_count = int(total_count.num * 0.6)
    return need_count


# sdk del and add at random
def sdk_change(results, total_count, online_count):
    while True:
        now_hour = datetime.datetime.now().hour
        differ_num = online_count - need_online_num(now_hour, total_count)
        # log.logger.info("need_online_num, total_count, len(results), differ_num", need_online_num(now_hour, total_count),
        #                 total_count.num, len(results), differ_num)
        print ("need_online_num, total_count, len(results), differ_num"), need_online_num(now_hour,
                                                                                          total_count), total_count.num, len(
            results), differ_num

        if differ_num > 0:
            result_num = 0
            while True:
                result = results[result_num]
                print "result", result
                # info_online = orm.session.query(Online).filter_by(peer_id=result.peer_id).all()
                # if len(info_online) > 0:
                orm.session.query(Online).filter(Online.peer_id == result.peer_id).delete()
                differ_num -= 1
                result_num += 1
                print "differ_num >0, result_num", differ_num, result_num
                if differ_num == 0 or result_num == (len(results) - 1):
                    break
            orm.session.commit()
            orm.session.close()
            log.logger.info("differ_num >0 commit")

        if differ_num <= 0:
            result_num = 0
            while True:
                result = results[result_num].peer_id
                print result
                if len(orm.session.query(Online).filter_by(peer_id=result).all()) == 0:
                    online = Online(peer_id=result.peer_id, sdk_version=result.sdk_version, public_ip=result.public_ip,
                                    public_port=result.public_port, private_ip=result.private_ip,
                                    private_port=result.private_port,
                                    nat_type=result.nat_type, stun_ip=result.stun_ip, isp_id=result.isp_id,
                                    province_id=result.province_id,
                                    lsm_free=result.lsm_free, lsm_total=result.lsm_total, disk_total=result.disk_total,
                                    disk_free=result.disk_free)
                    orm.session.add(online)
                    differ_num += 1
                    result_num += 1
                    print "differ_num <0, result_num", differ_num, result_num
                if differ_num == 0 or result_num == (len(result_num) - 1):
                    break
            orm.session.commit()
            orm.session.close()
            log.logger.info("differ_num <0 commit")
        time.sleep(3600)


if __name__ == "__main__":
    # sdk del and add at random,check every 1 h
    sdk_fluctuate(sdk_stable_online_rate=0.9)