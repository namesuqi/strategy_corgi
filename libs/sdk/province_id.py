# coding=utf-8
# author: JinYiFan

import random

# province_ids = ['110000', '310000', '320000', '330000', '350000', '370000', '410000', '420000', '430000', '440000',
#                 '510000']
province_ids = ['310000']
# province_rates = ['0.087', '0.223', '0.121', '0.111', '0.055', '0.065', '0.045', '0.04', '0.04', '0.165', '0.048']
province_rates = ['1']


def random_province_id():
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    item_provinceid = '110000'
    for item_provinceid, item_probability in zip(province_ids, province_rates):
        cumulative_probability += float(item_probability)
        if x < cumulative_probability:
            break
    return str(item_provinceid)


if __name__ == "__main__":
    for i in range(100):
        print random_province_id()
