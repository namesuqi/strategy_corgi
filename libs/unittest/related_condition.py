#!/usr/bin/python
# coding=utf-8
# related information of unittest
# author: JinYiFan

from libs.module.seeds import *
from libs.module.files import *
from libs.module.vod_push_file import *
from libs.common.path import *
from libs.sdk.file import *
from libs.const.config import *
from config import *

orm = MysqlORM()


def wait_for_second(wait_time):
    time.sleep(wait_time)


def change_config(push_download_bandwidth, seed_download_bandwidth, file_count, peer_count):
    """
    修改config文件的参数配置
    :param push_download_bandwidth: push下载带宽(Mbps)
    :param seed_download_bandwidth: seed下载带宽(Mbps)
    :param file_count: dir文件数目
    :param peer_count: 播放节点数目
    :return:
    """
    orm.session.query(Configs).filter(Configs.role == "push_download_bandwidth").update(
        {"content": push_download_bandwidth})
    orm.session.query(Configs).filter(Configs.role == "seed_download_bandwidth").update(
        {"content": seed_download_bandwidth})
    orm.session.query(Configs).filter(Configs.role == "peer_count").update(
        {"content": peer_count})
    orm.session.query(Configs).filter(Configs.role == "file_count").update(
        {"content": file_count})
    orm.session.commit()
    orm.session.close()


def add_one_file_in_dir(file_size, ppc):
    """
    dir-srv注册一个新文件
    :param file_size: 文件大小（B）
    :param ppc: ppc大小
    :return: 新文件的file_id
    """
    file = File(file_id=get_random_file_id(), file_size=file_size, url=get_random_file_url(), ppc=ppc, cppc=CPPC,
                piece_size=PSIZE)
    file_id = file.file_id
    orm.session.add(file)
    orm.session.commit()
    orm.session.close()
    return file_id


def add_multi_files_in_dir(file_count, ppc=None):
    """
    dir-srv新注册多个文件
    :param file_count: 新注册文件数目
    :param ppc: ppc大小（没有表示ppc随机）
    :return: 新注册文件的file_id
    """
    file_list = list()
    for i in range(file_count):
        if ppc is None:
            files = File(file_id=get_random_file_id(), file_size=get_random_file_size(), url=get_random_file_url(),
                         ppc=get_random_ppc(), cppc=CPPC, piece_size=PSIZE)
            orm.session.add(files)
            file_list.append(files.file_id)
        if ppc is not None:
            files = File(file_id=get_random_file_id(), file_size=get_random_file_size(), url=get_random_file_url(),
                         ppc=ppc, cppc=CPPC, piece_size=PSIZE)
            orm.session.add(files)
            file_list.append(files.file_id)
    orm.session.commit()
    orm.session.close()
    return file_list


def del_file_in_dir():
    """
    dir-srv删除已存在的文件（vod_push_srv和sdk已下载完成该文件）
    :return:
    """
    results = orm.session.query(Seed).filter_by(operation="download").all()
    for result in results:
        if len(orm.session.query(File).filter_by(file_id=result.file_id).all()) > 0:
            orm.session.query(File).filter_by(file_id=result.file_id).delete()
            orm.session.commit()
            orm.session.close()
            break


def control_dir_file_num(file_count):
    """
    控制dir-srv的文件总数
    :param file_count: 文件总数
    :return:
    """
    actual_count = orm.session.query(File).count()
    print actual_count
    if file_count > actual_count:
        for i in range(file_count - actual_count):
            files = File(file_id=get_random_file_id(), file_size=get_random_file_size(), url=get_random_file_url(),
                         ppc=get_random_ppc(), cppc=CPPC, piece_size=PSIZE)
            orm.session.add(files)
    if file_count < actual_count:
        results = orm.session.query(File).limit(actual_count - file_count).all()
        for result in results:
            orm.session.query(File).filter_by(file_id=result.file_id).delete()
    orm.session.commit()
    orm.session.close()


if __name__ == '__main__':
    # change_config(push_download_bandwidth=1000, seed_download_bandwidth=100,
    #               strategy_download_seed_num=600, file_count=100)
    # change_config(push_download_bandwidth=1000, seed_download_bandwidth=100,
    #               strategy_download_seed_num=600, file_count=2)

    # add_one_file_in_dir(file_size=1024 * 1024 * 1024, ppc=304)
    # print add_multi_files_in_dir(3, ppc=48)

    # del_file_in_dir()

    # control_dir_file_num(15)
    # import related_condition
    # print help(related_condition)
    add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=32)