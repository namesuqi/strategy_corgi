#!/usr/bin/python
# coding=utf-8
# combine data to logs for ELK analysis
# author: Su Qi

from libs.common.path import *
from libs.const.topics import *
import json
import redis
from libs.const.redis import *
from libs.const.config import *
from libs.module.files import *
import logging
from logging.handlers import RotatingFileHandler
from libs.module.seeds import *


# Deal with some of the combinations that need to be looked at for ELK to show
def monitor_combine_parameter():
    online_combine_log = LOGS_PATH + "/online_combine.log"
    logger = logging.getLogger()
    handler = RotatingFileHandler(online_combine_log, maxBytes=1024 * 1024 * 1024, backupCount=3)
    logger.addHandler(handler)
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    p = r.pubsub()
    p.subscribe(TOPIC_HEARTBEAT)
    while True:
        for i_item in p.listen():
            if 'data' in i_item:
                if type(i_item['data']) is str:
                    a = eval(i_item['data'])
                    province_id = str(a['province_id'])
                    isp_id = str(a['isp_id'])
                    timestamp = long(a['timestamp'])
                    peer_id = str(a['peer_id'])
                    user_id = peer_id[0:8]
                    nat = int(a['nat_type'])
                    sdk_version = str(a['sdk_version'])
                    combine = {
                        "timestamp": timestamp,
                        "peer_id": peer_id,
                        "user": user_id,
                        "nat_type": nat,
                        "sdk_version": sdk_version,
                        "province_id": province_id,
                        "isp_id": isp_id,
                        "province&isp": "{0}&{1}".format(province_id, isp_id),
                        "province&user": "{0}&{1}".format(province_id, user_id),
                        "province&version": "{0}&{1}".format(province_id, sdk_version),
                        "user&sdk": "{0}&{1}".format(user_id, sdk_version),
                        "sdk&nat": "{0}&{1}".format(sdk_version, nat)
                    }
                    combine_json = json.dumps(combine)
                    logger.warning(combine_json)
                handler.close()


# Deal with lsm_free for ELK to show
def monitor_lsm_free():
    lsm_free_log = LOGS_PATH + "/sdk_lsm_free.log"
    logger = logging.getLogger('lsm_free')
    handler = RotatingFileHandler(lsm_free_log, maxBytes=1024 * 1024 * 1024, backupCount=3)
    logger.addHandler(handler)
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    p = r.pubsub()
    p.subscribe(TOPIC_VOD_LSM)
    while True:
        for i_item in p.listen():
            if 'data' in i_item:
                if type(i_item['data']) is str:
                    a = eval(i_item['data'])
                    # lsm_free unit : B ---> MB
                    lsm_free = int(a['lsm_free']) / 1024 / 1024
                    if lsm_free <= 10:
                        lsm_free = LSM_FREE_LEVEL_A
                    elif 10 < lsm_free <= 50:
                        lsm_free = LSM_FREE_LEVEL_B
                    elif 50 < lsm_free <= 100:
                        lsm_free = LSM_FREE_LEVEL_C
                    elif 100 < lsm_free <= 300:
                        lsm_free = LSM_FREE_LEVEL_D
                    elif 300 < lsm_free <= 600:
                        lsm_free = LSM_FREE_LEVEL_E
                    else:
                        lsm_free = LSM_FREE_LEVEL_F
                    timestamp = long(a['timestamp'])
                    peer_id = str(a['peer_id'])
                    combine = {
                        "timestamp": timestamp,
                        "peer_id": peer_id,
                        "lsm_level": lsm_free
                    }
                    combine_json = json.dumps(combine)
                    logger.warning(combine_json)
                handler.close()


# deal with seed_table's sdk_fill_done, write the result to log
def monitor_seed_table_file_done():
    orm = MysqlORM()
    seed_file_done_log = LOGS_PATH + "/seed_file_done.log"
    fil = open(seed_file_done_log, "w")
    while True:
        seed_done_list = list()
        for file in orm.session.query(File).all():
            seed_done = orm.session.query(func.count('*')).filter(Seed.file_id == file.file_id,
                                                                  Seed.file_status == "done").scalar()
            orm.session.close()
            seed_done_list.append(int(seed_done))
            if seed_done > 0:
                combine = {
                    "timestamp": long(time.time() * 1000),
                    "file_id": file.file_id,
                    "seed_done_number": int(seed_done)
                }
                combine_json = json.dumps(combine)
                print combine_json
                fil.write(combine_json + "\n")
            fil.flush()
        time.sleep(10)


# p2p占比
def monitor_p2p_ratio():
    online_combine_log = LOGS_PATH + "/p2p_ratio.log"
    logger = logging.getLogger()
    handler = RotatingFileHandler(online_combine_log, maxBytes=1024 * 1024 * 1024, backupCount=3)
    logger.addHandler(handler)
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    p = r.pubsub()
    p.subscribe(TOPIC_FLOW)
    while True:
        for i_item in p.listen():
            if 'data' in i_item:
                if type(i_item['data']) is str:
                    p2p_data = eval(i_item['data'])
                    timestamp = long(p2p_data['timestamp'])
                    p2p_download = int(p2p_data['p2p_download'])
                    cdn_download = int(p2p_data['cdn_download'])
                    file_id = str(p2p_data['file_id'])
                    if p2p_download > 0 or cdn_download > 0:
                        p2p_combine = {
                            "timestamp": timestamp,
                            "p2p_download": p2p_download,
                            "cdn_download": cdn_download,
                            "file_id": file_id,
                            "p2p_ratio": float(p2p_download * 100 / (p2p_download + cdn_download))
                        }
                        combine_json = json.dumps(p2p_combine)
                        logger.warning(combine_json)
                handler.close()


# Wait for the directory to be created
def path_exists(path):
    while True:
        if not os.path.isdir(path):
            time.sleep(1)
            print "Wait for the directory to be created"
        else:
            print "The directory to be created"
            break

if __name__ == '__main__':
    monitor_seed_table_file_done()
