# coding=utf-8
# author: zeng yuetian


import time
import threading


class Base(object):
    pass


class Sub1(Base):
    def __init__(self):
        self.num = 2

    def run(self, num=10):
        for i in range(num):
            print(" from sub 1 - {0}".format(i))
            time.sleep(1)


class Sub2(Base):
    def __init__(self):
        self.num = 5

    def run(self, num=20):
        for i in range(num):
            print(" from sub 2 - {0}".format(i))
            time.sleep(1)

if __name__ == "__main__":
    monitors = [Sub1(), Sub2()]

    for monitor in monitors:
        t = threading.Thread(target=monitor.run, args=(monitor.num,))
        t.start()
        time.sleep(0.5)

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
