# coding=utf-8
# author: jinyifan

import random

chars = '0123456789ABCDEF'


def get_random_host_id():
    host_id_list = []
    for i in range(7):
        id = "".join(random.sample(chars, 2))
        host_id_list.append(id)
    host_id = ":".join(host_id_list)
    return host_id


if __name__ == "__main__":
    print get_random_host_id()
