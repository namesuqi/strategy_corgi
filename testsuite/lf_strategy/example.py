# !/usr/bin/python
# coding=utf-8
# author: JinYiFan

from libs.unittest.environment_prepare import *
from libs.unittest.live_related_condition import *
from libs.unittest.live_check_results import *
from libs.common.decorator import *
from libs.common.log import *
from libs.common.path import *
import unittest

log = Log("unittest_example", MONITOR_PATH + "/unittest_example.log")


class TestCorrectness(unittest.TestCase):
    @classmethod
    @func_doc
    def setUpClass(cls):
        """
        stop corgi and strategy supervisor
        """
        stop_corgi_all_process()
        time.sleep(10)
        stop_elk_seed_push_process()
        time.sleep(5)
        stop_read_main_task_process()
        time.sleep(5)

    @classmethod
    @func_doc
    def tearDownClass(cls):
        """
        stop all supervisor
        """
        # stop_all_supervisor()

    @func_doc
    def setUp(self):
        """
        empty redis, init and start strategy
        """
        reset_mysql_init()
        start_live_db_init()
        start_elk_seed_push_process()
        time.sleep(10)
        start_read_main_task_process()
        time.sleep(5)
        start_corgi_all_process()

    @func_doc
    def tearDown(self):
        """
        stop strategy
        """
        # stop_corgi_all_process()
        # time.sleep(5)
        # stop_elk_seed_push_process()
        # time.sleep(5)
        # stop_read_main_task_process()
        # time.sleep(5)

    @func_doc
    def testLFStrategyOnePeerOneFile(self):
        change_config(live_file_count=1, live_peer_count=1, rate_of_peer_and_file=1)
        start_live_config()
        log.logger.info("check lf strategy task num...")
        wait_for_second(5 * 600)
        sdk_download_task_num = check_sdk_download_task_num()
        log.logger.info("sdk_download_task_num is {0}".format(sdk_download_task_num))
