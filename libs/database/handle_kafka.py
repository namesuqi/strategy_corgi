# -*- coding: utf-8 -*-

"""
description:
    1.send logs to kafka
    2.get logs from kafka
"""

import io
import struct
import avro
import requests
import avro.io
import avro.schema
from pykafka import KafkaClient
from libs.const.vod_kafka import *
from pykafka.simpleconsumer import OffsetType

import time

# ---------------------------------------------------------------------------------------------------------------------

dis_id = "\r\r\r"  # dis-distinguish;

# ---------------------------------------------------------------------------------------------------------------------


def get_latest_schema_info(
        topic,
        schema_host=SCHEMA_HOST,
        schema_port=SCHEMA_PORT):
    # get latest schema format and schema_id of topic
    r = requests.get(
        "http://{0}:{1}/subjects/{2}-value/versions/latest".format(
            schema_host, schema_port, topic))
    if r.status_code == 200:
        rsp = r.json()
        return rsp["schema"], rsp["id"]
    else:
        raise ValueError(r.text)


def decode_by_avro(log_list, topic_schema, topic_schema_id):
    """
    avro logs
    :param log_list: [{}, {}, ...]
    :param topic_schema:
    :param topic_schema_id:
    :return:
    """
    bytes_header = "\x00" + struct.pack('>L', topic_schema_id)
    schema = avro.schema.parse(topic_schema)
    datum_writer = avro.io.DatumWriter(schema)

    bytes_encode = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_encode)

    for log in log_list:
        encoder.write_bytes(bytes_header)
        datum_writer.write(log, encoder)
        encoder.write_bytes(dis_id)
    bytes_logs = bytes_encode.getvalue()
    bytes_encode.close()

    bytes_logs = bytes_logs[1:]  # delete "\n"
    if len(dis_id) > 0:
        bytes_logs = bytes_logs[:-len(dis_id)]  # delete dis_id

    return bytes_logs

# ---------------------------------------------------------------------------------------------------------------------


# send logs to kafka
def write_logs_to_kafka_with_schema(
        topic,
        log_list,
        kafka_topic,
        topic_schema,
        topic_schema_id):
    if not isinstance(log_list, list):
        log_list = [log_list]

    bytes_logs = decode_by_avro(log_list, topic_schema, topic_schema_id)
    # client = KafkaClient(hosts=kafka_hosts)
    # kafka_topic = client.topics[topic]
    with kafka_topic.get_producer(max_queued_messages=10000, linger_ms=100)\
            as producer:
        for bytes_log in bytes_logs.split(dis_id + "\n"):
            producer.produce(bytes_log)


# send logs to kafka (without schema)
def write_logs_to_kafka(
        log_list,
        topic,
        kafka_hosts=KAFKA_HOSTS,
        schema_host=SCHEMA_HOST,
        schema_port=SCHEMA_PORT):
    # get latest schema of topic
    topic_schema, topic_schema_id = get_latest_schema_info(
        topic, schema_host=schema_host, schema_port=schema_port)

    # send avro logs to kafka
    start_ts = time.time()
    write_logs_to_kafka_with_schema(
        log_list,
        topic,
        topic_schema,
        topic_schema_id,
        kafka_hosts)
    end_ts = time.time()
    print "    send", len(log_list), topic, "log(s) cost", end_ts - start_ts, "second(s)"

# ---------------------------------------------------------------------------------------------------------------------


# get data from kafka

def new_consumer(topics, consumer_group, kafka_hosts):
    consumers = {}
    client = KafkaClient(hosts=kafka_hosts)
    for topic in topics:
        kafka_topic = client.topics[topic]
        consumer = kafka_topic.get_simple_consumer(
            consumer_group=consumer_group,
            consumer_timeout_ms=500,
            auto_commit_enable=True,
            auto_commit_interval_ms=1,
            auto_offset_reset=OffsetType.LATEST,
            reset_offset_on_start=True,
            consumer_id=consumer_group)
        consumers[topic] = consumer
        consumer.commit_offsets()
    return consumers


def search_schema(topics):
    schemas = {}
    for topic in topics:
        topic_schema, topic_schema_id = get_latest_schema_info(topic)
        schemas[topic] = [topic_schema, topic_schema_id]
    return schemas


def read_logs_from_kafka(consumers, schemas):
    collect_logs = []
    for topic, consumer in consumers.items():
        for message in consumer:
            if message is not None:
                msg_partition = message.partition.id
                msg_offset = message.offset
                bytes_msg = io.BytesIO(message.value[5:])
                decode_msg = avro.io.BinaryDecoder(bytes_msg)
                recode_msg = avro.io.DatumReader(
                    avro.schema.parse(schemas[topic][0])).read(decode_msg)
                # get partition，offset，value
                msg_collect = [msg_partition, msg_offset, recode_msg]
                collect_logs.append(msg_collect)
        collect_logs.sort(key=lambda x: x[2]["timestamp"])
        if len(collect_logs) is not 0:
            print "+++++++Topic: %s+++++++" % topic
            print "Consumed kafka logs count is:", len(collect_logs)
        for index, log in enumerate(collect_logs):
            print index, log
    return collect_logs

# ---------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    pass

