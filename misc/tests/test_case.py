#!/usr/bin/python
# coding=utf-8

import unittest
import time

from libs.unittest.environment_prepare import *


class Test(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    def setUp(self):
        print ("Test Start {0}".format(time.time()))
        clear_redis()
        start_seed_strategy()
        start_push_strategy()

    def tearDown(self):
        stop_seed_strategy()
        stop_push_strategy()
        print ("Test End {0}".format(time.time()))

    def test_add1(self):
        a = 2
        b = 3
        self.assertLess(a + b, 6)

    def test_add2(self):
        a = 2
        b = 3
        self.assertEqual(a + b, 6)


if __name__ == '__main__':
    # unittest.main()
    suitetest = unittest.TestSuite()
    suitetest.addTest(Test("test_add1"))
    suitetest.addTest(Test("test_add2"))
    # test_report(suitetest)
