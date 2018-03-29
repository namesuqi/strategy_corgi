# coding=utf-8
# author: zengyuetian


def func_doc(func):
    """
    print __doc__ string of test functions
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        print func.__doc__
        return func(*args, **kwargs)
    return wrapper
