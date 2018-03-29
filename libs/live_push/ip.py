# coding=utf-8
# author: JinYiFan

import random


def create_ip():
    l1 = random.randint(100, 192)
    l2 = random.randint(0, 255)
    l3 = random.randint(0, 255)
    l4 = random.randint(0, 255)
    ip = "{0}.{1}.{2}.{3}".format(l1, l2, l3, l4)
    return ip


if __name__ == "__main__":
    print create_ip()
