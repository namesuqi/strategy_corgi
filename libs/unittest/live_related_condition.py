# !/usr/bin/python
# coding=utf-8
# author: JinYiFan

from config import *
from libs.module.live_seeds import *
import time


def wait_for_second(wait_time):
    time.sleep(wait_time)


def change_config(live_file_count, live_peer_count, rate_of_peer_and_file):
    """
    修改config文件的参数配置
    :param live_file_count: 文件总数
    :param live_peer_count: 播放的节点总数
    :param rate_of_peer_and_file: 单个文件对应的播放节点数
    """
    orm.session.query(Configs).filter(Configs.role == "live_file_count").update(
        {"content": live_file_count})
    orm.session.query(Configs).filter(Configs.role == "live_peer_count").update(
        {"content": live_peer_count})
    orm.session.query(Configs).filter(Configs.role == "rate_of_peer_and_file").update(
        {"content": rate_of_peer_and_file})
    orm.session.commit()
    orm.session.close()


def change_peer_flow_to_0():
    """
    将peer的CDN和P2P流量设为0
    """
    orm.session.query(Live_Peer).update({"cdn": 0, "p2p": 0})
    orm.session.commit()
    orm.session.close()


def change_LF_flow_to_0():
    """
    将LF的CDN和P2P流量设为0
    """
    orm.session.query(Live_Seed).update({"upload": 0, "download": 0})
    orm.session.commit()
    orm.session.close()


def add_player(play_num):
    """
    增加播放节点
    :param play_num: 增加的播放节点数
    """
    peer_num_infos = orm.session.query(Live_Online).offset(200).limit(play_num).all()
    file_id = orm.session.query(Live_Peer).first().file_id

    num = 0
    for num in range(play_num):
        live_peer_sdk = Live_Peer(peer_id=peer_num_infos[num].peer_id, version=peer_num_infos[num].sdk_version,
                                  country=peer_num_infos[num].country, province_id=peer_num_infos[num].province_id,
                                  city_id=peer_num_infos[num].city_id, isp_id=peer_num_infos[num].isp_id,
                                  file_id=file_id, chunk_id=get_random_chunk_id(), operation=OPERATION, cdn=CDN,
                                  p2p=P2P, ssid=peer_num_infos[num].ssid, p2penable=P2PENABLE)
        orm.session.add(live_peer_sdk)
        num += 1
    orm.session.commit()
    orm.session.close()


def one_peer_multi_channel(channel_num):
    """
    一个播放节点播放多个频道
    :param channel_num: 一个播放节点播放的频道数
    """
    peer_info = orm.session.query(Live_Peer).first()
    file_info = orm.session.query(Live_File).offset(5).limit(channel_num).all()

    for num in range(channel_num - 1):
        live_peer_sdk = Live_Peer(peer_id=peer_info.peer_id, version=peer_info.version, country=peer_info.country,
                                  province_id=peer_info.province_id, city_id=peer_info.city_id, isp_id=peer_info.isp_id,
                                  file_id=file_info[num].file_id, chunk_id=get_random_chunk_id(), operation=OPERATION,
                                  cdn=CDN, p2p=P2P, ssid=peer_info.ssid, p2penable=P2PENABLE)
        orm.session.add(live_peer_sdk)
        num += 1
    orm.session.commit()
    orm.session.close()


def del_player(del_num):
    """
    删除播放节点
    :param del_num: 删除的播放节点数
    """
    peer_infos = orm.session.query(Live_Peer).all()
    session_ids = list()
    for peer_info in peer_infos:
        session_ids.append(peer_info.ssid)

    num = 0
    for num in range(del_num):
        orm.session.query(Live_Peer).filter_by(ssid=session_ids[num]).delete()
        num += 1
    orm.session.commit()
    orm.session.close()


def del_seed(del_num):
    """
    删除雷锋节点
    :param del_num: 删除的雷锋节点数
    """
    seed_infos = orm.session.query(Live_Seed).all()
    session_ids = list()
    for seed_info in seed_infos:
        session_ids.append(seed_info.ssid)
    num = 0
    for num in range(del_num):
        orm.session.query(Live_Seed).filter_by(ssid=session_ids[num]).delete()
        num += 1
    orm.session.commit()
    orm.session.close()


if __name__ == "__main__":
    del_seed(20)
    # add_player(3)
    # one_peer_multi_channel(3)
    # del_player(2)
