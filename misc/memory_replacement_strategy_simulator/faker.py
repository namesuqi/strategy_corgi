# coding=utf-8
# simulate sdk behavior
# author: myn
import time
import math
from config_loader import Loader
import urllib2


import sys
sys.stdout = open("zyt.log", 'w')

loader = Loader()
config_info = loader.load_config_file()


chunks_per_query = config_info['chunks_per_query']
cppc = config_info['cppc']
push_host = config_info['push_host']
headers_push = config_info['headers_push']
re_request_interval = config_info['sdk_re_request_interval']


def fake_sdk(
        process_num,
        sdk_no,
        file_size,
        file_id,
        ppc,
        logger,
        start_chunk_id):
    chunk_gross = int(math.ceil(file_size * 1024 * 1024 / int(ppc) / 1392))

    start_time = time.time()
    while start_chunk_id < chunk_gross:
        # send request from here
        send_req_time = time.time()
        if start_chunk_id + chunks_per_query > chunk_gross:
            last_query_chunks = chunk_gross % chunks_per_query
            get_file_url = \
                "http://{0}/push/files/{1}/chunks/{2}_{3}/pieces/{4}".format(
                    push_host, file_id, chunk_gross - last_query_chunks,
                    last_query_chunks, cppc)
            # end_chunk_id = chunk_gross
        else:
            get_file_url = \
                "http://{0}/push/files/{1}/chunks/{2}_{3}/pieces/{4}".format(
                    push_host, file_id, start_chunk_id, chunks_per_query, cppc)
            # end_chunk_id = start_chunk_id + chunks_per_query

        req = urllib2.Request(get_file_url)
        try:
            response = urllib2.urlopen(req)
            receive_req_time = time.time()
            if response.getcode() == 200:
                start_chunk_id += chunks_per_query
                time.sleep(max(0.095 - (time.time() - send_req_time), 0))
            if process_num % 2 == 0 and start_chunk_id % 120 == 0:
                print("P{process}-T{thread}:{cid}-{cost}\n".format(
                    process=process_num,
                    thread=sdk_no,
                    cid=start_chunk_id,
                    cost=time.time() - start_time))
                start_time = time.time()
        except urllib2.HTTPError as e:
            code = e.code
            receive_req_time = time.time()
            if code == 503:
                print("503 ***************************************************\n")
                time.sleep(max(re_request_interval -
                               (time.time() - send_req_time), 0))
