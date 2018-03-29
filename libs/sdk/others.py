# coding=utf-8
# author: JinYiFan
# live sdk related

import random

country = 'CN'
city_id = 440100
cppc = 1


# session_id
chars = '0123456789abcdef'


def create_ssid():
    ssid = ""
    for i in range(32):
        ssid += chars[random.randint(0, 15)]
    return ssid


if __name__ == "__main__":
    print create_ssid()
