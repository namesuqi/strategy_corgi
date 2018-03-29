# coding=utf-8
# author: JinYiFan

import random

# isp_ids = ['100017', '100025', '100026', '0', '1000143', '100063', '1000140', '100020', '1000139', '100027', '100076']
isp_ids = ['100026']

# isp_rates = ['0.536', '0.162', '0.217', '0.037', '0.033', '0.0022', '0.002', '0.002', '0.002', '0.0023', '0.002']
isp_rates = ['1']


def random_isp_id():
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    item_isp = '100017'
    for item_isp, item_probability in zip(isp_ids, isp_rates):
        cumulative_probability += float(item_probability)
        if x < cumulative_probability:
            break
    return str(item_isp)


if __name__ == "__main__":
    for i in range(100):
        print random_isp_id()
