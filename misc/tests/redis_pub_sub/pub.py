# coding=utf-8
"""''
Created on 2015-9-9

@author: Administrator
"""
import redis

pool = redis.ConnectionPool(host='192.168.2.50', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
p = r.pubsub()
while True:
    input = raw_input("publish:")
    if input == 'over':
        print '停止发布'
        break
    r.publish('redisChat', input)
