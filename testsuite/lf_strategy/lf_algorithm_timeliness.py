#!/usr/bin/python
# coding=utf-8
# author: SuQi

from libs.unittest.environment_prepare import *
from libs.unittest.live_related_condition import *
from libs.unittest.lf_timeliness_related import *
from libs.common.decorator import *
from libs.common.log import *
from libs.common.path import *
import unittest
import time

log = Log("lf_unittest_timeliness", MONITOR_PATH + "/lf_unittest_timeliness.log")


class TestTimeliness(unittest.TestCase):
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
        delete_file()
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
        # delete_file()
        # stop_corgi_all_process()
        # time.sleep(5)
        # stop_elk_seed_push_process()
        # time.sleep(5)
        # stop_read_main_task_process()
        # time.sleep(5)

    @func_doc
    def testLFStrategyCalculateCycleTime(self):
        """
        策略计算周期为60s
        """

        change_config(live_file_count=1, live_peer_count=1, rate_of_peer_and_file=1)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(5 * 60)
        self.assertTrue(check_lf_strategy_compute_cycle_time() == 60000, "LF_strategy start calculate time not in time")

    @func_doc
    def testLFStrategyDownloadStartTime(self):
        """
        策略启动后收到汇报,会在4min内生成频道的download任务
        """

        change_config(live_file_count=1, live_peer_count=1, rate_of_peer_and_file=1)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(5 * 60)
        strategy_calculate_start_time = check_lf_strategy_start_time()
        strategy_start_download_time = check_lf_strategy_sdk_download_start_time()
        self.assertTrue(strategy_start_download_time - strategy_calculate_start_time <= 4 * 60 * 1000,
                        "LF_strategy download_task start not in time")

    @func_doc
    def testLFStrategyDeleteStartTime(self):
        """
        策略5min内没有收到播放节点的汇报,会下发delete任务
        """

        change_config(live_file_count=1, live_peer_count=1, rate_of_peer_and_file=1)
        start_live_config()
        log.logger.info("check lf strategy start time ...")
        wait_for_second(5 * 60)
        del_player(1)
        timestamp = int(round(time.time() * 1000))
        self.assertTrue(check_lf_strategy_sdk_delete_start_time() - timestamp <= 5 * 60 * 1000,
                        "strategy delete_task start not in time")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestTimeliness("testLFStrategyDownloadStartTime"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # unittest.main()
