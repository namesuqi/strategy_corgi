# coding=utf-8
# author: zengyuetian

import random


def create_port(total):
    """
    create port for sdk report
    :param total:
    :return:
    """
    num = 0
    ports = list()
    for port in range(40000, 50000):
        ports.append(port)
        num += 1
        if num >= total:
            return ports


ports = create_port(10000)


def get_random_port():
    return random.choice(ports)


if __name__ == "__main__":
    for i in range(10):
        print get_random_port()
