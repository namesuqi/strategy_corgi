# coding=utf-8
# author: zengyuetian

import random


# def create_version(total):
#     """
#     create version for sdk
#     :param total:
#     :return:
#     """
#     versions = list()
#     majors = [4]
#     minors = range(2)
#     builds = range(5)
#     num = 0
#     for major in majors:
#         for minor in minors:
#             for build in builds:
#                 version = "{0}.{1}.{2}".format(major, minor, build)
#                 # print "{0}.{1}.{2}".format(major, minor, build)
#                 versions.append(version)
#                 num += 1
#                 if num >= total:
#                     return versions
#
#
# versions = create_version(10)


versions = ['4.1.3', '4.1.11', '4.2.0']


def get_random_version():
    return random.choice(versions)


if __name__ == "__main__":
    for i in range(5):
        print get_random_version()
