#!/usr/bin/python
# coding=utf-8
# author: JinYiFan

from libs.unittest.environment_prepare import *
from libs.unittest.live_related_condition import *
from libs.unittest.live_check_results import *
from libs.common.decorator import *
from libs.common.log import *
from libs.common.path import *
import unittest
import time

log = Log("lf_unittest_correctness", MONITOR_PATH + "/lf_unittest_correctness.log")


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
    def testFlowZero(self):
        """
        当有播放节点,流量统计(cdn + p2p)不大于0时,策略不会下发任务
        """
        change_config(live_file_count=1, live_peer_count=1, rate_of_peer_and_file=1)
        start_live_config()
        wait_for_second(2)
        change_peer_flow_to_0()
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_download_task_num(), [], "lf_strategy should have no tasks")

    @func_doc
    def testAddOnePeer(self):
        """
        当播放节点4个,策略已拉入50个雷锋时,增加1个播放节点,策略不会下发任务(无非法雷锋)
        """
        change_config(live_file_count=1, live_peer_count=4, rate_of_peer_and_file=4)
        start_live_config()
        wait_for_second(4 * 60)
        sdk_download_task_num = check_sdk_download_task_num()
        log.logger.info("sdk_download_task_num is {0}".format(sdk_download_task_num))
        add_player(1)
        log.logger.info("add one peer...")
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_download_task_num(), sdk_download_task_num, "lf_strategy should have no more tasks")

    @func_doc
    def testOnePeerMultiFiles(self):
        """
        当1个节点播放多个频道时, 策略可根据频道正常下发任务
        """
        change_config(live_file_count=5, live_peer_count=5, rate_of_peer_and_file=1)
        start_live_config()
        wait_for_second(10 * 60)
        self.assertEqual(check_sdk_download_task_num(), [50, 50, 50, 50, 50], "lf_strategy should have download tasks")

    @func_doc
    def testTenPeers(self):
        """
        当有播放节点数且小于等于10个,无雷锋节点时,策略会一次性下发50个download任务
        """
        change_config(live_file_count=1, live_peer_count=10, rate_of_peer_and_file=10)
        start_live_config()
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_download_task_num(), [50], "lf_strategy should have download tasks")

    @func_doc
    def testMoreThanTenPeers(self):
        """
        当播放节点数大于10个,无雷锋节点时,策略会一次性下发5*play个download任务
        """
        change_config(live_file_count=1, live_peer_count=15, rate_of_peer_and_file=15)
        start_live_config()
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_download_task_num(), [75], "lf_strategy should have download tasks")

    @func_doc
    def testNoPeerWithLF(self):
        """
        当无播放节点,有雷锋节点时,策略会下发delete任务
        """
        change_config(live_file_count=1, live_peer_count=1, rate_of_peer_and_file=1)
        start_live_config()
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_download_task_num(), [50], "lf_strategy should have download tasks")
        del_player(1)
        log.logger.info("del peers")
        wait_for_second(6 * 60)
        self.assertEqual(check_sdk_delete_task_num(), [50], "lf_strategy should have del tasks")

    @func_doc
    def testDelInvalidLFs(self):
        """
        策略每次在计算下发任务时会对非法雷锋节点下发清退任务
        """
        change_config(live_file_count=1, live_peer_count=1, rate_of_peer_and_file=1)
        start_live_config()
        wait_for_second(5 * 60)
        self.assertEqual(check_sdk_download_task_num(), [50], "lf_strategy should have download tasks")
        change_LF_flow_to_0()
        log.logger.info("change LF flow to 0...")
        wait_for_second(3 * 60)
        self.assertEqual(check_sdk_delete_task_num(), [50], "lf_strategy should have delete tasks")
        wait_for_second(2 * 60)
        self.assertEqual(check_sdk_download_task_num(), [100], "lf_strategy should have download tasks")
        change_LF_flow_to_0()
        log.logger.info("change LF flow to 0...")
        wait_for_second(3 * 60)
        self.assertEqual(check_sdk_delete_task_num(), [100], "lf_strategy should have delete tasks")
        wait_for_second(2 * 60)
        self.assertEqual(check_sdk_download_task_num(), [150], "lf_strategy should have download tasks")


if __name__ == "__main__":
    unittest.main()
