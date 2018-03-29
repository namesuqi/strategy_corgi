# coding=utf-8
# author: zengyuetian

import random

nat_types = [0, 1, 3, 4, 5]
nat_type_rates = ['0.001', '0.34', '0.59', '0.06', '0.009']


def get_random_nat_type():
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    item_nattype = 0
    for item_nattype, item_probability in zip(nat_types, nat_type_rates):
        cumulative_probability += float(item_probability)
        if x < cumulative_probability:
            break
    return str(item_nattype)


if __name__ == "__main__":
    for i in range(100):
        print get_random_nat_type()
