#!/usr/bin/python
# coding=utf-8
# general environment
# author: Su Qi

from rediscluster import *
from libs.const.redis import *
from libs.module.inits import *
from libs.const.supervisor import *
import xmlrpclib
import paramiko

s_main = xmlrpclib.Server(CORGI_SUPERVISOR)
s_seed_push = xmlrpclib.Server(ELK_PUSH_SEED_SUPERVISOR)
s_read_task = xmlrpclib.Server(READ_TASK_MAIN_SUPERVISOR)


# start all supervisor
def start_all_supervisor():
    start_elk_seed_push_process()
    start_corgi_all_process()
    # start_read_main_task_process()


# stop all supervisor
def stop_all_supervisor():
    stop_corgi_all_process()
    stop_read_main_task_process()
    stop_elk_seed_push_process()


# supervisor start corgi
def start_corgi_all_process():
    s_main.supervisor.startAllProcesses()


# supervisor stop corgi
def stop_corgi_all_process():
    s_main.supervisor.stopAllProcesses()


# clear seeds_strategy's redis
def clear_redis():
    redis_connect = StrictRedisCluster(startup_nodes=REDIS_NODES)
    for key in redis_connect.keys():
        redis_connect.delete(key)


# supervisor start seeds_strategy
def start_seed_strategy():
    s_seed_push.supervisor.startProcess('seeds_strategy')


# supervisor stop seeds_strategy
def stop_seed_strategy():
    s_seed_push.supervisor.stopProcess('seeds_strategy')


# supervisor start push_strategy
def start_push_strategy():
    s_seed_push.supervisor.startProcess('push_strategy')


# supervisor stop push_strategy
def stop_push_strategy():
    s_seed_push.supervisor.stopProcess('push_strategy')


# supervisor start ELK_server
def start_elk_seed_push_process():
    s_seed_push.supervisor.startAllProcesses()


# supervisor stop ELK_server
def stop_elk_seed_push_process():
    s_seed_push.supervisor.stopAllProcesses()


# supervisor start Read_main_task
def start_read_main_task_process():
    s_read_task.supervisor.startAllProcesses()


# supervisor stop Read_main_task
def stop_read_main_task_process():
    s_read_task.supervisor.stopAllProcesses()


# mysql init table set to 1
def reset_mysql_init():
    orm = MysqlORM()
    orm.session.query(Inits).filter_by(role='init').update({'num': 1})
    orm.session.commit()


# start db_init vod
def start_vod_db_init():
    # s_main.supervisor.startProcess('db_init')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.3.217', 22, 'root', 'root', compress=True)
    client.exec_command('/root/corgi/db_init.py vod')
    print "init success"
    client.close()


# start db_init live
def start_live_db_init():
    # s_main.supervisor.startProcess('db_init')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.3.217', 22, 'root', 'root', compress=True)
    client.exec_command('/root/corgi/db_init.py live')
    print "init success"
    client.close()


# stop db_init
def stop_db_init():
    s_main.supervisor.stopProcess('db_init')


# supervisor start config vod
def start_vod_config():
    # s_main.supervisor.startProcess('config')
    # start db_init
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.3.217', 22, 'root', 'root', compress=True)
    client.exec_command('/root/corgi/config.py vod')
    client.close()


# supervisor start config live
def start_live_config():
    # s_main.supervisor.startProcess('config')
    # start db_init
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.3.217', 22, 'root', 'root', compress=True)
    client.exec_command('/root/corgi/config.py live')
    client.close()


# supervisor stop config
def stop_config():
    s_main.supervisor.stopProcess('config')


def start_sdk_fluctuate():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.3.217', 22, 'root', 'root', compress=True)
    client.exec_command('/root/corgi/sdk_fluctuate.py &')
    client.close()


# delete strategy_file
def delete_file():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("192.168.1.188", 22, "root", "root", compress=True)
    str_command = "rm -rf /root/dslive/lf_strategy.out"
    stdin, stdout, stderr = client.exec_command(str_command)
    print stdout.read()
    client.close()

if __name__ == '__main__':
    # stop_read_main_task_process()
    # clear_redis()
    # print s_main.system.listMethods()
    # s_main.supervisor.startAllProcesses()
    # start_corgi_all_process()
    # s_main.supervisor.stopAllProcesses()
    # start_config()
    start_sdk_fluctuate()
