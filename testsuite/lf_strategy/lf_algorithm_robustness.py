#!/usr/bin/python
# coding=utf-8
# author: Su Qi

from libs.unittest.lf_robustness_related import *
from libs.unittest.environment_prepare import *
from libs.unittest.live_related_condition import *
from libs.unittest.live_check_results import *
from libs.common.decorator import *
from libs.common.log import *
from libs.common.path import *
import unittest
import time

log = Log("lf_unittest_correctness", MONITOR_PATH + "/lf_unittest_correctness.log")


class TestRobustness(unittest.TestCase):
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
        stop_corgi_all_process()
        time.sleep(5)
        stop_elk_seed_push_process()
        time.sleep(5)
        stop_read_main_task_process()
        time.sleep(5)

    @func_doc
    def testLFStrategyEachDownloadNum(self):
        """
        策略每次下发download任务数目不超过10*play个
        """
        change_config(live_file_count=1, live_peer_count=4, rate_of_peer_and_file=4)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(6 * 60)
        num_list = check_lf_strategy_each_download_num()
        for each_download_num in num_list:
            self.assertTrue(each_download_num <= 10 * check_lf_strategy_player_count(),
                            "LF_strategy should issue download_task 10*play")

    @func_doc
    def testLFStrategyPlayLess10(self):
        """
        当播放节点数小于等于10,p2p_rate<=0.4时,策略会拉入雷锋,直至download任务50个
        """
        change_config(live_file_count=1, live_peer_count=8, rate_of_peer_and_file=8)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(5 * 60)
        del_seed(40)
        seed_table_num = check_lf_seed_table_count()
        log.logger.info("sdk_download_task_num is {0}".format(seed_table_num))
        wait_for_second(5 * 60)
        seed_num = check_lf_seed_table_count()
        log.logger.info("seed_num is {0}".format(seed_num))
        self.assertTrue(seed_num == 50, "lf_strategy should have seed 50 items")

    @func_doc
    def testLFStrategyPlayMore10(self):
        """
        当播放节点数大于10,p2p_rate<=0.4时,策略会拉入雷锋,直至download任务数范围为[4*play,6*play]
        """
        change_config(live_file_count=1, live_peer_count=12, rate_of_peer_and_file=12)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(5 * 60)
        play_count = check_lf_strategy_player_count()
        log.logger.info("play_count is {0}".format(play_count))
        sdk_download_task_num = check_sdk_download_task_num()
        log.logger.info("sdk_download_task_num is {0}".format(sdk_download_task_num))
        del_seed(40)
        seed_table_num = check_lf_seed_table_count()
        log.logger.info("seed_table_num is {0}".format(seed_table_num))
        wait_for_second(5 * 60)
        seed_num = check_lf_seed_table_count()
        log.logger.info("seed_num is {0}".format(seed_num))
        self.assertTrue(4 * play_count <= seed_num <= 6 * play_count, "lf_strategy seed num error ")

    @func_doc
    def testLFStrategyP2PMiddleDownload(self):
        """
        当0.4<p2p_rate<=0.85时,策略下一个计算周期下发download任务数不超过(lf数*10%)/p2p_rate个
        """
        change_config(live_file_count=1, live_peer_count=12, rate_of_peer_and_file=12)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(5 * 60)
        play_count = check_lf_strategy_player_count()
        log.logger.info("play_count is {0}".format(play_count))
        sdk_download_task_num = check_sdk_download_task_num()
        log.logger.info("sdk_download_task_num is {0}".format(sdk_download_task_num))
        del_seed(15)
        seed_table_num = check_lf_seed_table_count()
        log.logger.info("seed_table_num is {0}".format(seed_table_num))
        wait_for_second(5 * 60)
        sdk_download_num = check_sdk_download_task_num()
        self.assertTrue(sdk_download_task_num[0] + seed_table_num / 7 <= sdk_download_num[0] <= 10 * play_count,
                        "lf_strategy seed num error ")

    @func_doc
    def testLFStrategyDownloadNum(self):
        """
        当播放节点10个,策略已拉入50个雷锋,增加1个播放节点,策略会再拉入雷锋不超过5个
        """
        change_config(live_file_count=1, live_peer_count=10, rate_of_peer_and_file=10)
        start_live_config()
        wait_for_second(5 * 60)
        check_download_num = check_sdk_download_task_num()
        self.assertTrue(check_download_num == 50, "lf_strategy should have download tasks")
        add_player(1)
        log.logger.info("add 1 peer")
        wait_for_second(5 * 60)
        self.assertTrue(50 < check_lf_seed_table_count() <= 55, "lf_strategy should add download tasks")

    @func_doc
    def testLFStrategyP2PMiddleDelete(self):
        """
        当0.4<p2p_rate<=0.85时,策略下发delete任务数为max(lf_valid-10*play,0)
        """
        change_config(live_file_count=1, live_peer_count=5, rate_of_peer_and_file=5)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(5 * 60)
        sdk_download_task_num = check_lf_seed_table_count()
        log.logger.info("sdk_download_task_num is {0}".format(sdk_download_task_num))
        del_seed(15)
        lf_valid_num = check_lf_seed_table_count()
        log.logger.info("sdk_download_table is {0}".format(lf_valid_num))
        wait_for_second(5 * 60)
        self.assertTrue(0 <= check_sdk_delete_task_num() <= abs(lf_valid_num - 10 * 5),
                        "lf_strategy seed num error ")

    @func_doc
    def testLFStrategyP2PHighDelete(self):
        """
        当p2p_rate>0.85且有雷锋节点超过50个时,策略下发delete任务数为max(lf_valid*5%,lf_valid-10*play)
        """
        change_config(live_file_count=1, live_peer_count=12, rate_of_peer_and_file=12)
        start_live_config()
        log.logger.info("check LF_strategy start time ...")
        wait_for_second(5 * 60)
        sdk_download_task_num = check_lf_seed_table_count()
        log.logger.info("sdk_download_task_num is {0}".format(sdk_download_task_num))
        del_seed(5)
        lf_valid_num = check_lf_seed_table_count()
        log.logger.info("sdk_download_table is {0}".format(lf_valid_num))
        if lf_valid_num > 50:
            wait_for_second(5 * 60)
            self.assertTrue(0 <= check_sdk_delete_task_num() <= abs(lf_valid_num * 0.05),
                            "lf_strategy seed num error ")

    @func_doc
    def testLFStrategyDeleteNum(self):
        """
        当播放节点5个,雷锋节点稳定时, 减少1个播放节点,策略会下发清退雷锋不超过max(lf_valid*5%,lf_valid-50)
        """
        change_config(live_file_count=1, live_peer_count=5, rate_of_peer_and_file=5)
        start_live_config()
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_download_task_num(), [50], "lf_strategy should have download tasks")
        del_player(1)
        log.logger.info("del 1 peer")
        lf_valid_num = check_lf_seed_table_count()
        log.logger.info("sdk_download_table is {0}".format(lf_valid_num))
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_delete_task_num() <= lf_valid_num * 0.05, "lf_strategy should add delete tasks")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestRobustness("testLFStrategyP2PMiddleDownload"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
    # unittest.main()
