# coding=utf-8
# author: JinYiFan

import random

chars = '0123456789ABCDEF'
charsall = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
length = len(chars) - 1

PPC = 32
CPPC = 1
OPERATION = "add"
CDN = 6842880
P2P = 0
P2PENABLE = "true"


def get_random_live_file_id():
    file_id = ""
    for i in range(32):
        file_id += chars[random.randint(0, length)]
    return file_id


def get_random_live_file_url():
    # user = ""
    name = ""
    for i in range(5):
        # user += random.choice(charsall)
        name += random.choice(charsall)

    file_url = "http://test.live.entropycode.net/live/{0}.flv".format(name)
    return file_url


def get_random_chunk_id():
    chunk_id = random.randint(10000, 100000)
    return chunk_id

if __name__ == "__main__":
    for i in range(300):
        print get_random_chunk_id()
