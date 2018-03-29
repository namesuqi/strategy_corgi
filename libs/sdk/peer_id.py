# coding=utf-8
# author: JinYiFan
# create peer_id according to init table

import random

user_id = "00000004"
chars = '0123456789ABCDEF'
length = len(chars) - 1


def create_peer_id(online_num):
    peer_id_online_list = []
    for n in range(online_num):
        peer_id = user_id
        for i in range(24):
            peer_id += chars[random.randint(0, length)]

        peer_id_online_list.append(peer_id)
    # print "online peer_id:", peer_id_online_list

    # peer_id_peer_list = peer_id_online_list[0:peer_num]
    # print "peer peer_id:", peer_id_peer_list

    return peer_id_online_list


if __name__ == "__main__":
    print create_peer_id(2)
