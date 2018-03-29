# coding=utf-8
# singleton design pattern
# author: Zeng YueTian


def singleton(cls):
    instances = dict()

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton
