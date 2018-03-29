#!/usr/bin/python
# coding=utf-8
# author: JinYiFan

import sys

sys.path.append(sys.path[0] + '/../..')
print sys.path

from libs.unittest.environment_prepare import *
from libs.unittest.related_condition import *
from libs.unittest.check_results import *
from sdk_fluctuate import *
from libs.common.decorator import *
from libs.common.log import *
import unittest

log = Log("unittest_robustness", MONITOR_PATH + "/unittest_robustness.log")


class TestTimeliness(unittest.TestCase):
    @classmethod
    @func_doc
    def setUpClass(cls):
        """
        start corgi supervisor
        """
        stop_corgi_all_process()
        time.sleep(5)
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
        time.sleep(30)
        stop_elk_seed_push_process()
        time.sleep(20)
        clear_redis()

    @func_doc
    def testPushDistributeParallelCount_1(self):
        """
        vod_push策略每次下发的push_prefetch_task数目不超过2个
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=10, peer_count=0)
        start_vod_config()
        log.logger.info("test push_distribute_parallel_count: push_prefetch_task...")
        wait_for_second(10 * 60)
        self.assertIsNone(check_strategy_prefetch_parallel_num(),
                          "push_push_task parallel_num should be no more than 2")

    @func_doc
    def testPushDistributeParallelCount_2(self):
        """
        vod_push策略每次下发的sdk_download_task数目不超过74个
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=10, peer_count=0)
        start_vod_config()
        log.logger.info("test push_distribute_parallel_count: sdk_download_task...")
        wait_for_second(3 * 60 * 60)
        self.assertIsNone(check_strategy_download_parallel_num(),
                          "push_push_task parallel_num should be no more than 74")

    @func_doc
    def testPushDistributeCount_1(self):
        """
        当dir-srv有1个1GB的文件，PPC=304，vod_push策略下发sdk_download_task的seed总数小于等于855
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=304)
        log.logger.info("test push_distribute_count: sdk_download_task num...")
        wait_for_second(20 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 855, "sdk_download_task num should be no more than 855")

    @func_doc
    def testPushDistributeCount_2(self):
        """
        当dir-srv有1个1GB的文件，PPC=32，vod_push策略下发sdk_download_task的seed总数小于等于90
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=32)
        log.logger.info("test push_distribute_count: sdk_download_task num...")
        wait_for_second(10 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 90, "sdk_download_task num should be no more than 90")

    @func_doc
    def testPushDistributeCount_3(self):
        """
        当dir-srv有10个1GB-20GB的文件，PPC=32，vod_push策略下发sdk_download_task的seed总数小于等于900
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_multi_files_in_dir(file_count=10, ppc=32)
        log.logger.info("test push_distribute_count: sdk_download_task num...")
        wait_for_second(3 * 60 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 900, "sdk_download_task num should be no more than 900")

    @func_doc
    def testPushDistributeCount_4(self):
        """
        当dir-srv有100个1GB-20GB的文件，PPC从32-304不等，vod_push策略下发sdk_download_task的seed总数小于85500
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_multi_files_in_dir(file_count=100, ppc=None)
        log.logger.info("test push_distribute_count: sdk_download_task num...")
        wait_for_second(24 * 60 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 85500, "sdk_download_task num should be no more than 85500")

    @func_doc
    def testPushDistributeNoRepeat(self):
        """
        当push-srv已缓存文件并汇报，则vod_push策略不会重复下发该文件的push_prefetch_task
        """
        new_file_id = add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=32)
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=5, peer_count=0)
        start_vod_config()
        log.logger.info("test push_distribute_count: push_prefetch_task not repeat...")
        wait_for_second(10 * 60)
        self.assertFalse(check_push_prefetch_task_repeat(new_file_id), "push_prefetch_task should not repeat")

    @func_doc
    def testPushDistributeCount_OneFile(self):
        """
        dir-srv有1个文件，PPC=304，当固定1000节点（总节点的1%）随机上下线波动时，vod_push策略下发单个文件的seed任务总数收敛，且不小于684
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=304)
        log.logger.info("test push_distribute_count: sdk_download_task num...")
        time.sleep(10 * 60)
        start_sdk_fluctuate()
        wait_for_second(60 * 60)
        sdk_download_task_one_file_num = check_sdk_download_task_num()
        log.logger.info("sdk_download_task num is {0}".format(sdk_download_task_one_file_num))
        self.assertTrue(684 <= check_sdk_download_task_num() <= 2000, "sdk_download_task_num should convergence")

    @func_doc
    def testPushDistributeCount_MultiFiles_1(self):
        """
        dir-srv有10个文件，PPC从32-304不等，当固定10000节点（总节点的10%）随机上下线波动时，vod_push策略下发单个文件的seed任务总数不小于45 * (ppc/16)*0.8
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        file_ids = add_multi_files_in_dir(file_count=10, ppc=None)
        log.logger.info("test push_distribute_count: sdk_download_task num...")
        start_sdk_fluctuate()
        log.logger.info("start sdk_fluctuate...")
        wait_for_second(10 * 60 * 60)
        min_count = min(check_file_seed_download_num(file_ids))
        max_count = max(check_file_seed_download_num(file_ids))
        log.logger.info(
            "min file_seed_download_num is {0}, max file_seed_download_num is {1}".format(min_count, max_count))
        self.assertTrue(72 < min_count < 2000, "sdk_download_task_num should convergence")
        self.assertTrue(684 < max_count < 2000, "sdk_download_task_num should convergence")

    @func_doc
    def testPushDistributeCount_MultiFiles_2(self):
        """
        dir-srv有100个文件，PPC从32-304不等，当固定10,000节点（总节点的10%）随机上下线波动时，vod_push策略下发单个文件的seed任务总数不小于45 * (ppc/16)*0.8
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        file_ids = add_multi_files_in_dir(file_count=100, ppc=None)
        log.logger.info("test push_distribute_count: sdk_download_task num...")
        start_sdk_fluctuate()
        log.logger.info("start sdk_fluctuate...")
        wait_for_second(24 * 60 * 60)
        min_count = min(check_file_seed_download_num(file_ids))
        max_count = max(check_file_seed_download_num(file_ids))
        log.logger.info(
            "min file_seed_download_num is {0}, max file_seed_download_num is {1}".format(min_count, max_count))
        self.assertTrue(72 < min_count < 5000, "sdk_download_task_num should convergence")
        self.assertTrue(684 < max_count < 5000, "sdk_download_task_num should convergence")


if __name__ == '__main__':
    unittest.main()
    # testsuite = unittest.TestSuite()
    # testsuite.addTest(TestTimeliness("testPushDistributeParallelCount_1"))
    # runner = unittest.TextTestRunner()
    # runner.run(testsuite)
