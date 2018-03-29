# coding=utf-8
# author: JinYiFan

import random

chars = '0123456789ABCDEF'
charsall = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
length = len(chars) - 1


def get_random_file_id():
    file_id = ""
    for i in range(32):
        file_id += chars[random.randint(0, length)]
    return file_id


def get_random_file_url():
    # user = ""
    name = ""
    for i in range(5):
        # user += random.choice(charsall)
        name += random.choice(charsall)

    file_url = "http://vod4ktest.cloutropy.com/4k/{0}.mp4".format(name)
    return file_url


# file_size:B, range from 1GB to 20GB
def get_random_file_size():
    file_size = random.randint(1073741824, 21474836480)
    return file_size


# ppc range from 32 to 304
def get_random_ppc():
    while True:
        ppc = random.randint(32, 305)
        if ppc % 16 == 0:
            return ppc

if __name__ == "__main__":
    for i in range(300):
        print get_random_ppc()
