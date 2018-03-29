#!/usr/bin/python
# coding=utf-8

from libs.database.handle_kafka import *


def write_to_kafka(topic, datas):
    client = KafkaClient(hosts=KAFKA_HOSTS)
    kafka_topic = client.topics[topic]
    schema, schema_id = get_latest_schema_info(topic)
    write_logs_to_kafka_with_schema(topic, datas, kafka_topic, schema, schema_id)

push_prefetch = [
    {
        "file_type": "m3u8",
        "timestamp": long(time.time() * 1000),
        # "file_url": "http://vod4ktest.cloutropy.com/4k/vttHU.mp4",
        "file_url": "http://vod4ktest.cloutropy.com/4k/QXVs2.mp4",
        "push_ip": "118.190.153.230",
        "priority": 1,
        "piece_size": 1396,
        # "file_id": "D605388FDABC1E5BCB8D5C36C515E1FC",
        "file_id": "76B1B5B1F35F8996CBBEEDB113D7D281",
        "cppc": 1,
        "file_size": 21474836480,
        "operation": "prefetch",
        "push_id": "00:16:3E:06:C3:A6",
        "ppc": 304
    }
]

push_delete = [
    {
        "timestamp": long(time.time() * 1000),
        "push_ip": "118.190.153.230",
        "priority": 1,
        "file_id": "CC7EF1E8FAF87B5966F00BAA2DABABA5",
        "operation": "delete",
        "push_id": "00:16:3E:06:C3:A6"
    }
]


task_vod_sdk_download = {
        "file_id": "77BFD961FA87492A860E211E7E5600D2",
        "file_size": 775134238,
        "file_url": "http://1111111.flv",
        "ppc": 304,
        "cppc": 1,
        "piece_size": 11111,
        "priority": 10,
        "operation": 'download',
        "timestamp": long(round(time.time() * 1000)),
        "peer_id": "76B1B5B1F35F8996CBBEEDB113D7D281",
        "push_ip": "192.168.1.214",
        "push_port": 80,
        "isp_id": 'zz',
        "province_id": 'zz'
}


task_vod_sdk_del = {
    "file_id": "77BFD961FA87492A860E211E7E5600p2",
    "priority": 10,
    "operation": 'del',
    "timestamp": long(round(time.time() * 1000)),
    "peer_id": "76B1B5B1F35F8996CBBEEDB113D7D281",
    "isp_id": 'zz',
    "province_id": '440000'
}


live_task = {
    "topic": "sdk_directional_task_live",
    "file_id": "77BFD961FA87492A860E211E7E5600p2",
    "peer_id": "76B1B5B1F35F8996CBBEEDB113D7D281",
    "timestamp": long(round(time.time() * 1000)),
    "operation": "download"
}

write_to_kafka('sdk_directional_task_live', live_task)
# write_to_kafka('task_vod_push_delete', push_delete)
print 11
