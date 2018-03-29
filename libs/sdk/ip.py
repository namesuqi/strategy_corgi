# coding=utf-8
# author: zengyuetian

import random


# Private address
# A class 10.0.0.0--10.255.255.255
# B class 172.16.0.0--172.31.255.255
# C class 192.168.0.0--192.168.255.255


def create_address_for_class(l1, l2, l3, l4, total):
    """
    create ip address
    :param l1:
    :param l2:
    :param l3:
    :param l4:
    :param total:
    :return:
    """
    ips = list()
    num = 0
    for a in l1:
        for b in l2:
            for c in l3:
                for d in l4:
                    ip = "{0}.{1}.{2}.{3}".format(a, b, c, d)
                    ips.append(ip)
                    num += 1
                    if num >= total:
                        return ips


def create_private_address_for_a_class(total):
    """
    create private ip for A class
    :param total:
    :return:
    """
    l1 = [10]
    l2 = range(256)
    l3 = range(256)
    l4 = range(256)
    return create_address_for_class(l1, l2, l3, l4, total)


def create_private_address_for_b_class(total):
    """
    create private ip for B class
    :param total:
    :return:
    """
    l1 = [172]
    l2 = range(16, 32)
    l3 = range(256)
    l4 = range(256)
    return create_address_for_class(l1, l2, l3, l4, total)


def create_private_address_for_c_class(total):
    """
    create private ip for C class
    :param total:
    :return:
    """
    l1 = [192]
    l2 = [168]
    l3 = range(256)
    l4 = range(256)
    return create_address_for_class(l1, l2, l3, l4, total)


def create_public_address_for_a_class(total):
    """
    create public ip for A class
    :param total:
    :return:
    """
    l1 = [11]
    l2 = range(256)
    l3 = range(256)
    l4 = range(256)
    return create_address_for_class(l1, l2, l3, l4, total)


public_ips = create_public_address_for_a_class(10000)
private_ips = create_private_address_for_c_class(10000)


def get_random_public_ip():
    return random.choice(public_ips)


def get_random_private_ip():
    return random.choice(private_ips)


if __name__ == "__main__":
    for i in range(10):
        print get_random_public_ip()
        print get_random_private_ip()
