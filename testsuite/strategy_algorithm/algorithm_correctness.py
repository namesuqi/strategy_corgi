# !/usr/bin/python
# coding=utf-8
# author: JinYiFan

import sys

sys.path.append(sys.path[0] + '/../..')
print sys.path

from libs.unittest.environment_prepare import *
from libs.unittest.related_condition import *
from libs.unittest.check_results import *
from libs.common.decorator import *
from libs.common.log import *
import unittest

log = Log("unittest_correctness", MONITOR_PATH + "/unittest_correctness.log")


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
        clear_redis()

    @classmethod
    @func_doc
    def tearDownClass(cls):
        """
        stop all supervisor
        """
        stop_all_supervisor()

    @func_doc
    def setUp(self):
        """
        empty redis, init and start strategy
        """
        reset_mysql_init()
        start_vod_db_init()
        start_elk_seed_push_process()
        time.sleep(10)
        start_corgi_all_process()

    @func_doc
    def tearDown(self):
        """
        stop strategy
        """
        stop_corgi_all_process()
        time.sleep(5)
        stop_elk_seed_push_process()
        time.sleep(5)
        clear_redis()

    @func_doc
    def testPushDistributeOneFile(self):
        """
        当dir-srv只有1个文件，vod_push策略下发1个push_prefetch_task和1个文件的sdk_download_task
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=1, peer_count=0)
        start_vod_config()
        log.logger.info("check push_prefetch_task file num...")
        wait_for_second(5 * 60)
        push_prefetch_task_file_num = check_push_prefetch_task_num()
        log.logger.info("push_prefetch_task file num is {0}".format(push_prefetch_task_file_num))
        self.assertEqual(1, push_prefetch_task_file_num, "push_prefetch_task file num should be 1")

        log.logger.info("check sdk_download_task file num...")
        wait_for_second(10 * 60)
        sdk_download_task_file_num = check_sdk_download_task_file_num()
        log.logger.info("sdk_download_task file num is {0}".format(sdk_download_task_file_num))
        self.assertEqual(1, sdk_download_task_file_num, "sdk_download_task file num should be 1")

    @func_doc
    def testPushDistributeMultiFiles_1(self):
        """
        当dir-srv有10个文件，vod_push策略下发10个push_prefetch_task和10个文件的sdk_download_task
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=10, peer_count=0)
        start_vod_config()
        log.logger.info("check push_prefetch_task file num...")
        wait_for_second(10 * 60)
        push_prefetch_task_file_num = check_push_prefetch_task_num()
        log.logger.info("push_prefetch_task file num is {0}".format(push_prefetch_task_file_num))
        self.assertEqual(10, push_prefetch_task_file_num, "push_prefetch_task file num should be 10")

        log.logger.info("check sdk_download_task file num...")
        wait_for_second(3 * 60 * 60)
        sdk_download_task_file_num = check_sdk_download_task_file_num()
        log.logger.info("sdk_download_task file num is {0}".format(sdk_download_task_file_num))
        self.assertEqual(10, sdk_download_task_file_num, "sdk_download_task file num should be 10")

    @func_doc
    def testPushDistributeMultiFiles_2(self):
        """
        当dir-srv有100个文件，vod_push策略下发100个push_prefetch_task和100个文件的sdk_download_task
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=100, peer_count=0)
        start_vod_config()
        log.logger.info("check push_prefetch_task file num...")
        wait_for_second(2 * 60 * 60)
        push_prefetch_task_file_num = check_push_prefetch_task_num()
        log.logger.info("push_prefetch_task file num is {0}".format(push_prefetch_task_file_num))
        self.assertEqual(100, push_prefetch_task_file_num, "push_prefetch_task_num should be 100")

        log.logger.info("check sdk_download_task file num...")
        wait_for_second(24 * 60 * 60)
        sdk_download_task_file_num = check_sdk_download_task_file_num()
        log.logger.info("sdk_download_task file num is {0}".format(sdk_download_task_file_num))
        self.assertEqual(100, sdk_download_task_file_num, "sdk_download_task file_num should be 100")

    @func_doc
    def testPushDistributeOrder(self):
        """
        检查vod_push策略下发sdk_download_task顺序：优先文件 > 点播文件 > size大小
        """
        stop_corgi_all_process()
        time.sleep(10)
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=4, peer_count=1)
        start_vod_config()
        stop_elk_seed_push_process()
        time.sleep(10)
        start_elk_seed_push_process()
        time.sleep(10)
        start_corgi_all_process()
        log.logger.info("check push distribute order...")
        wait_for_second(60 * 60)
        self.assertTrue(check_sdk_download_task_order(), "sdk_download_task order is wrong")


if __name__ == "__main__":
    unittest.main()
