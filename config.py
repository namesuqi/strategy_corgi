#!/usr/bin/python
# coding=utf-8
# __author__ = JinYiFan

from libs.module.configs import *
from libs.module.files import *
from libs.module.onlines import *
from libs.module.peers import *
from libs.sdk.file import *
from libs.const.config import CPPC, PSIZE, DURATION, OPERATION, PLAY_TYPE, ERROR_TYPE
from libs.module.live_onlines import *
from libs.module.live_files import *
from libs.module.live_peers import *
from libs.sdk.live_file import *
import datetime
import requests
import sys

orm = MysqlORM()


# read config table information in mysql
def read_config():
    global push_download_bandwidth, seed_download_bandwidth, sdk_review_duration, push_review_duration, peer_count, \
        file_count, push_write_num, file_write_num, file_status_write_number, sdk_write_number, live_file_count, \
        live_peer_count, rate_of_peer_and_file
    results = orm.session.query(Configs).all()
    orm.session.close()
    for result in results:
        if result.role == "push_download_bandwidth":
            push_download_bandwidth = int(result.content)
        elif result.role == "seed_download_bandwidth":
            seed_download_bandwidth = int(result.content)
        elif result.role == "sdk_review_duration":
            sdk_review_duration = int(result.content)
        elif result.role == "push_review_duration":
            push_review_duration = int(result.content)
        elif result.role == "peer_count":
            peer_count = int(result.content)
        elif result.role == "file_count":
            file_count = int(result.content)
        elif result.role == "push_write_num":
            push_write_num = int(result.content)
        elif result.role == "file_write_num":
            file_write_num = int(result.content)
        elif result.role == "file_status_write_number":
            file_status_write_number = int(result.content)
        elif result.role == "sdk_write_number":
            sdk_write_number = int(result.content)
        elif result.role == "live_file_count":
            live_file_count = int(result.content)
        elif result.role == "live_peer_count":
            live_peer_count = int(result.content)
        elif result.role == "rate_of_peer_and_file":
            rate_of_peer_and_file = int(result.content)
    return push_download_bandwidth, seed_download_bandwidth, sdk_review_duration, push_review_duration, peer_count, \
           file_count, push_write_num, file_write_num, file_status_write_number, sdk_write_number, live_file_count, \
           live_peer_count, rate_of_peer_and_file


push_download_bandwidth, seed_download_bandwidth, sdk_review_duration, push_review_duration, peer_count, file_count, \
push_write_num, file_write_num, file_status_write_number, sdk_write_number, live_file_count, live_peer_count, rate_of_peer_and_file = \
    read_config()


# write files table
def write_file_table(file_count):
    for i in range(file_count):
        files = File(file_id=get_random_file_id(), file_size=get_random_file_size(), url=get_random_file_url(),
                     ppc=get_random_ppc(), cppc=CPPC, piece_size=PSIZE)
        orm.session.add(files)
    orm.session.commit()
    orm.session.close()
    print("reset file table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# write peer table
def write_peer_table(peer_count):
    peer_num_infos = orm.session.query(Online).limit(peer_count).all()

    for num in range(peer_count):
        print peer_num_infos[num].peer_id
        peer_info = peer_num_infos[num]
        file_info = orm.session.query(File).first()

        peer_sdk = Peer(peer_id=peer_info.peer_id, sdk_version=peer_info.sdk_version, public_ip=peer_info.public_ip,
                        public_port=peer_info.public_port, private_ip=peer_info.private_ip,
                        private_port=peer_info.private_port, nat_type=peer_info.nat_type,
                        stun_ip=peer_info.stun_ip, isp_id=peer_info.isp_id, province_id=peer_info.province_id,
                        duration=DURATION, file_id=file_info.file_id, seeds_download=0, seeds_upload=0,
                        cdn_download=0, p2p_download=0, operation=OPERATION, play_type=PLAY_TYPE,
                        error_type=ERROR_TYPE, file_size=file_info.file_size, url=file_info.url, ppc=file_info.ppc,
                        cppc=file_info.cppc, piece_size=file_info.piece_size)
        orm.session.add(peer_sdk)
    orm.session.commit()
    orm.session.close()
    print("write peer table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# config priority_file
def priority_file_config():
    if orm.session.query(File).count() > 1:
        file_info = orm.session.query(File)[1]
        orm.session.close()
        priority_file_id = file_info.file_id

        req_config = requests.get('http://192.168.1.188:9998/vodpush/control/hfile?cmd=add&type=file&value={0}'.format(
            priority_file_id))
        print("file {0} has been hfile, status code is {1}".format(priority_file_id, req_config.status_code))


# --------------------------------------live parts
# write live files table
def write_live_file_table(live_file_count):
    for i in range(live_file_count):
        live_files = Live_File(file_id=get_random_live_file_id(), ppc=PPC, cppc=CPPC, url=get_random_live_file_url())
        orm.session.add(live_files)
    orm.session.commit()
    orm.session.close()
    print("reset live file table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# write live_peer table
def write_live_peer_table(live_peer_count, rate_of_peer_and_file):
    peer_num_infos = orm.session.query(Live_Online).limit(live_peer_count).all()
    file_num_infos = orm.session.query(Live_File).limit(live_peer_count/rate_of_peer_and_file).all()

    num = 0
    for num in range(live_peer_count):
        file_num = num/rate_of_peer_and_file

        live_peer_info = peer_num_infos[num]
        live_file_info = file_num_infos[file_num]
        print live_peer_info.peer_id
        print live_file_info.file_id

        live_peer_sdk = Live_Peer(peer_id=live_peer_info.peer_id, version=live_peer_info.sdk_version, country=live_peer_info.country,
                                  province_id=live_peer_info.province_id, city_id=live_peer_info.city_id, isp_id=live_peer_info.isp_id,
                                  file_id=live_file_info.file_id, chunk_id=get_random_chunk_id(), operation=OPERATION, cdn=CDN, p2p=P2P,
                                  ssid=live_peer_info.ssid, p2penable=P2PENABLE)
        orm.session.add(live_peer_sdk)
        num += 1
    orm.session.commit()
    orm.session.close()
    print("write live peer table done", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    if sys.argv[1] == "vod":
        read_config()
        write_file_table(file_count)
        write_peer_table(peer_count)
        priority_file_config()

    if sys.argv[1] == "live":
        read_config()
        write_live_file_table(live_file_count)
        write_live_peer_table(live_peer_count, rate_of_peer_and_file)
