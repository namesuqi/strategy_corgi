#!/usr/bin/python
# coding=utf-8
# 1.read strategy tasks from kafka
# 2.execute tasks and write results to mysql
# 3.add access file time dynamics
# author = 'myn'
# version: stable-3.0
import threading
import json
from misc.mock_tool.obtain_file_time_mocker import *
from config import *
from libs.common.path import *
from libs.strategy_executor.deal_tasks_from_kafka import *
from libs.kibana_show_log.kibana_analyse_log import path_exists
# from libs.unittest.check_results import strategy_download_seed_num

push_change_status = {}
sdk_change_status_queue = []
count = 0
sdk_downloading = []
push_prefetch_downloading = []
push_file_for_calculate = {}
push_file_queue = []


def write_tasks_info_to_mysql(tasks):
    orm = MysqlORM()
    global push_file_for_calculate
    global count
    global push_prefetch_downloading

    for task in tasks:
        task_info = task[2]

        # push del task
        if len(task_info) == PUSH_DEL_LEN:
            deal_push_del_tasks(task_info)
            log.logger.info('push delete successfully at {0}'.format(time.time()))

        # push prefetch task
        if len(task_info) == PUSH_PREFETCH_LEN:
            file_id = task_info['file_id']
            push_id = task_info['push_id']
            file_size = task_info['file_size']

            vod_push_file_info = orm.session.query(Vod_Push_File).filter_by(file_id=file_id, push_id=push_id).all()
            # print vod_push_file_info
            if len(vod_push_file_info) == 0 and (file_id, push_id) not in push_file_for_calculate:
                log.logger.info('get push prefetch task at time:{0}'.format(time.time()))
                deal_push_prefetch_tasks(task_info, file_id, push_id, file_size)
                # add downloading task to push_prefetch_downloading,and start downloading
                prefetch_info = [file_id, push_id]
                push_prefetch_downloading.append(prefetch_info)
                mutex.acquire()
                push_file_for_calculate[(file_id, push_id)] = file_size
                mutex.release()
                if len(push_file_for_calculate) < 2:
                    thread_push_prefetch = threading.Thread(target=push_state_change_mocker, args=())
                    thread_push_prefetch.start()
                else:
                    mutex.acquire()
                    push_file_queue.append({(file_id, push_id): file_size})
                    mutex.release()
        # sdk del file t.ask
        if len(task_info) == SDK_DEL_LEN:
            deal_sdk_del_tasks(task_info)

        # sdk download file task
        if len(task_info) == SDK_DOWNLOAD_LEN:
            file_id = task_info['file_id']
            peer_id = task_info['peer_id']
            file_size = task_info['file_size']
            ppc = task_info['ppc']

            info_online = orm.session.query(Online).filter_by(peer_id=peer_id).all()
            info_seed = orm.session.query(Seed).filter_by(peer_id=peer_id, file_id=file_id).all()
            # sdk in table online and not in table seed
            if len(info_seed) == 0 and len(info_online) > 0:
                log.logger.info('seed start get file time at {0}'.format(time.time()))
                log.logger.info('------main count is {0}'.format(count))
                deal_sdk_download_tasks(task_info, peer_id)
                mutex.acquire()
                if count < PUSH_CONCURRENT_VOLUME:

                    # add downloading task to sdk_downloading
                    sdk_downloading.append(peer_id)

                    # change sdk_status after sdk_get_file_done
                    timer = threading.Timer(sdk_get_file_time_consume(file_size, ppc), sdk_state_change_mocker,
                                            (file_id, peer_id))
                    timer.start()
                    count += 1

                # if count >= PUSH_CONCURRENT_VOLUME,add sdk to sdk_change_status_queue
                else:
                    sdk_change_status_queue.append(
                        {'file_id': file_id, 'peer_id': peer_id, 'file_size': file_size, 'ppc': ppc})
                mutex.release()
    orm.session.close()


def push_state_change_mocker():
    global push_prefetch_downloading
    if len(push_file_for_calculate) != 0:

        for info, file_size in push_file_for_calculate.items():
            time_file_download_use = push_prefetch_time_consume(file_size)
            log.logger.info('file: {0} will cost time: {1}s to finish'.format(info[0], time_file_download_use))

            time.sleep(time_file_download_use)
            mutex.acquire()
            push_file_for_calculate.clear()
            mutex.release()
            push_prefetch_downloading.remove([info[0], info[1]])
            log.logger.info('push finish get file time at:{0}'.format(time.time()))
            orm.session.query(Vod_Push_File).filter_by(file_id=info[0], push_id=info[1]).update({'flag': 'end'})
            orm.session.query(Vod_Push_File).filter_by(file_id=info[0], push_id=info[1]).update({'behavior': 'in'})
            orm.session.commit()
            orm.session.close()
            while len(push_file_queue) > 0:
                mutex.acquire()
                push_file_for_calculate.update(push_file_queue[0])
                push_file_queue.remove(push_file_queue[0])
                mutex.release()
                push_state_change_mocker()


def sdk_state_change_mocker(file_id, peer_id):
    global count
    global sdk_change_status_queue
    global sdk_downloading

    # change done_seed status
    orm.session.query(Seed).filter_by(file_id=file_id, peer_id=peer_id).update({'file_status': 'done'})
    orm.session.commit()
    orm.session.close()
    log.logger.info("file_id:{0}, peer_id:{1} has been changed to done".format(file_id, peer_id))
    mutex.acquire()
    sdk_downloading.remove(peer_id)
    count -= 1
    log.logger.info('------sdk_stat_change_mocker count is {0}'.format(count))
    if len(sdk_change_status_queue) != 0:
        count += 1
        log.logger.info('------sdk_change_status_queue count is {0}'.format(count))
        sdk = sdk_change_status_queue[0]
        sdk_downloading.append(sdk['peer_id'])

        sdk_change_status_queue.remove(sdk)
        timer = threading.Timer(sdk_get_file_time_consume(sdk['file_size'], sdk['ppc']), sdk_state_change_mocker,
                                (sdk['file_id'], sdk['peer_id']))
        timer.start()
        log.logger.info("file_id:{0}, peer_id:{1} will be changed".format(sdk['file_id'], sdk['peer_id']))
    mutex.release()


def seed_get_file_cost():
    orm = MysqlORM()
    while True:
        done_list = orm.session.query(Seed).filter_by(file_status='done').all()
        orm.session.close()
        if len(done_list) >= 500:
            log.logger.info('{0} seed done at time:{1}'.format(500, time.time()))
            break
        time.sleep(1)


# statistics effective tasks
def accept_valid_tasks(tasks, map_debug):
    for task_debug in tasks:
        task_info_debug = task_debug[2]
        if len(task_info_debug) == SDK_DOWNLOAD_LEN:
            file_id_debug = task_info_debug['file_id']
            peer_id_debug = task_info_debug['peer_id']
            # map here is for avoid duplication
            map_debug[(file_id_debug, peer_id_debug)] = 1
    log.logger.info('~~~~~~~~~~~~~~~~~~~~~~~~~useful tasks sdk add; {0}'.format(len(map_debug)))


def monitor_push_bandwidth():
    """
    如果有push文件或SDK文件下载,即表示push带宽被占用,把带宽信息写入log,用于Kibana展示带宽信息
    :return: n.a.
    """
    # Wait for the directory to be created
    path_exists(LOGS_PATH)
    push_bandwidth_log = LOGS_PATH + "/push_bandwidth.log"
    fil = open(push_bandwidth_log, "w")
    # bandwidth unit: Mbps
    push_prefetch_bandwidth = min(push_download_bandwidth, cdn_upload_bandwidth)
    # seed_get_file_max_speed: bps ---> Mbps
    sdk_download_bandwidth = min(seed_get_file_max_speed / 1000000.0, seed_download_bandwidth * 1.0,
                                 push_upload_bandwidth * 1.0)
    while True:
        # handle SDK downloading
        if len(sdk_downloading) > 0:
            sdk_download_number = len(sdk_downloading)
            sdk_download_info = {
                "timestamp": long(time.time() * 1000),
                "download_number": sdk_download_number,
                "sdk_download_bandwidth": sdk_download_bandwidth,
                "push_upload_bandwidth": min(sdk_download_bandwidth * sdk_download_number, push_upload_bandwidth)
            }
            sdk_download_info_json = json.dumps(sdk_download_info)
            print sdk_download_info_json
            fil.write(sdk_download_info_json + "\n")
            fil.flush()

        # handle push prefetch
        if len(push_prefetch_downloading) > 0:
            push_prefetch_number = len(push_prefetch_downloading)
            push_prefetch_info = {
                "timestamp": long(time.time() * 1000),
                "prefetch_number": push_prefetch_number,
                "push_prefetch_bandwidth": push_prefetch_bandwidth
            }
            push_prefetch_info_json = json.dumps(push_prefetch_info)
            print push_prefetch_info_json
            fil.write(push_prefetch_info_json + "\n")
            fil.flush()
        time.sleep(1)


if __name__ == '__main__':
    get_tasks_interval = 2
    debug_map = {}
    log = Log("strategy_executor", MONITOR_PATH + "/strategy_executor.log")
    mutex = threading.Lock()

    # Establish connections to kafka
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
    t2 = threading.Thread(target=seed_get_file_cost, args=())
    t2.start()
    t3 = threading.Thread(target=monitor_push_bandwidth, args=())
    t3.start()

    while True:
        received_all_tasks = read_logs_from_kafka(new_consumers, schemas)
        accept_valid_tasks(received_all_tasks, debug_map)
        t1 = threading.Thread(target=write_tasks_info_to_mysql, args=(received_all_tasks,))
        t1.start()
        # write_tasks_info_to_mysql(received_all_tasks)
        log.logger.info('=================Kiroff Report===================>>>>>')
        time.sleep(get_tasks_interval)
