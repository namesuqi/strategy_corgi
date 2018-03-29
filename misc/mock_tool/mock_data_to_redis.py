#!/usr/bin/python
# coding=utf-8

import redis

pool = redis.ConnectionPool(host='192.168.3.178', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)

keys = r.keys()
print type(keys)
print keys

province_ids = ['110000', '310000', '320000', '330000', '350000', '370000', '410000', '420000', '430000', '440000',
                '510000']
isp_ids = ['100017', '100025', '100026', '0', '1000143', '100063', '1000140', '100020', '1000139', '100027', '100076']

for province in province_ids:
    for isp in isp_ids:
        r.set('ALLOW_WEIGTH-{0}_{1}'.format(province, isp), '{}')
