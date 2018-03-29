#!/usr/bin/python
# coding=utf-8
# author: myn
# read data from redis-cluster and write them to mysql
# these seeds are real seeds

from rediscluster import StrictRedisCluster
from libs.common.log import Log
from libs.common.path import MONITOR_PATH
from libs.const.redis import *
from libs.database.mysql_orm import MysqlORM
from libs.module.seed_pool import Seed_pool
from misc.mock_tool.mock_strategy_task import obtain_peer_id_from_table
import time
import sys

orm = MysqlORM()


def read_seed_pool_redis():
    peer_ids_in_redis = []
    seeds_add_to_mysql = []
    file_ids = []
    redis_nodes = [
        {'host': SEED_POOL_REDIS_CLUSTER_HOST_1,
         'port': SEED_POOL_REDIS_CLUSTER_PORT_1},
        {'host': SEED_POOL_REDIS_CLUSTER_HOST_2,
         'port': SEED_POOL_REDIS_CLUSTER_PORT_2},
        {'host': SEED_POOL_REDIS_CLUSTER_HOST_3,
         'port': SEED_POOL_REDIS_CLUSTER_PORT_3}
    ]

    peer_ids_in_mysql = obtain_peer_id_from_table(Seed_pool)
    redis_connect = StrictRedisCluster(startup_nodes=redis_nodes)

    # get keys contain TSGO
    for key in redis_connect.keys():
        # key: {TSGO
        if key.find('TSGO') == 1:
            file_ids.append(key)

    if file_ids:
        # get file id, currently we only have one channel, so we only handle
        # file_ids[0]
        for file_id in file_ids:
            file_id_write_to_mysql = file_id.split("_")[2]
            # get value by key
            selected_seeds = redis_connect.smembers(file_id)
            log.logger.info('redis seeds num:{0}'.format(len(selected_seeds)))
            for seed in selected_seeds:
                # eval it from string to dictionary
                seed_info = eval(seed)
                peer_id = seed_info['peer_id']
                peer_ids_in_redis.append(peer_id)
                if peer_id not in peer_ids_in_mysql:
                    sdk_version = seed_info['version']
                    private_ip = seed_info['privateIP']
                    private_port = seed_info['privatePort']
                    public_ip = seed_info['publicIP']
                    public_port = seed_info['publicPort']
                    nat_type = seed_info['natType']
                    stun_ip = seed_info['stunIP']
                    isp_id = seed_info['isp_id']
                    province_id = seed_info['province_id']
                    ppc = seed_info['ppc']
                    cppc = seed_info['cppc']
                    seed_redis = (Seed_pool(peer_id=peer_id,
                                            sdk_version=sdk_version,
                                            public_ip=public_ip,
                                            public_port=public_port,
                                            private_ip=private_ip,
                                            private_port=private_port,
                                            nat_type=nat_type,
                                            stun_ip=stun_ip,
                                            isp_id=isp_id,
                                            province_id=province_id,
                                            ppc=ppc,
                                            cppc=cppc,
                                            file_id=file_id_write_to_mysql))
                    orm.session.add(seed_redis)
                    seeds_add_to_mysql.append(seed_redis)
        orm.session.commit()
        orm.session.close()
        log.logger.info('add {0} seeds to mysql'.format(len(seeds_add_to_mysql)))
        # del seeds expired(in mysql but not in redis)
        peer_ids_in_mysql_after_add = obtain_peer_id_from_table(Seed_pool)
        for peer in peer_ids_in_mysql_after_add:
            if peer not in peer_ids_in_redis:
                orm.session.query(Seed_pool).filter_by(
                    peer_id=peer).delete()
        orm.session.commit()
        orm.session.close()
    else:
        # if seeds list in redis is empty, clean MySQL
        log.logger.info('no seeds in redis so we clean table seed_pool ')
        orm.session.query(Seed_pool).filter().delete()
        orm.session.commit()
        orm.session.close()


if __name__ == '__main__':
    query_frequency = 30
    log = Log("seedpool_transport", MONITOR_PATH + "/seedpool_transport.log")
    while True:
        read_seed_pool_redis()
        time.sleep(query_frequency)
