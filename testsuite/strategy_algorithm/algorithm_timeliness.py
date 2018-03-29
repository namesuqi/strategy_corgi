#!/usr/bin/python
# coding=utf-8
# author: JinYiFan , SuQi

from libs.unittest.environment_prepare import *
from libs.unittest.related_condition import *
from libs.unittest.check_results import *
from libs.unittest.timeliness_related import *
from libs.common.log import *
import unittest
from libs.common.decorator import *

log = Log("main", MONITOR_PATH + "/main.log")


class TestTimeliness(unittest.TestCase):
    @classmethod
    @func_doc
    def setUpClass(cls):
        """
        start corgi supervisor
        """
        # stop_all_supervisor()
        stop_corgi_all_process()
        stop_read_main_task_process()
        time.sleep(10)
        stop_elk_seed_push_process()
        time.sleep(10)
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
        start_read_main_task_process()

    @func_doc
    def tearDown(self):
        """
        stop strategy
        """
        stop_corgi_all_process()
        stop_read_main_task_process()
        time.sleep(10)
        stop_elk_seed_push_process()
        time.sleep(10)
        clear_redis()

    @func_doc
    def testPushStrategyStartCalculateTime(self):
        """
        策略启动后整分开始计算
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=1, peer_count=1)
        start_vod_config()
        wait_for_second(3 * 60)
        expect_start_time = expect_strategy_start_calculate_time()
        real_start_time = check_strategy_start_calculate_time()
        self.assertTrue(real_start_time == expect_start_time, "strategy start calculate time not in time")

    @func_doc
    def testPushPrefetchRegisterNewOneFile(self):
        """
        dir-srv注册一个新文件，vod_push策略在2min内生成新文件的push_prefetch_task
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_multi_files_in_dir(file_count=1)
        wait_for_second(4 * 60)
        strategy_initialize_time = check_strategy_initialize_time()
        strategy_prefetch_time = check_strategy_push_prefetch_time()
        self.assertTrue(strategy_prefetch_time - strategy_initialize_time <= 120000,
                        "strategy push_prefetch_task issued not in time")

    @func_doc
    def testPushDownloadRegisterNewOneFile(self):
        """
        dir-srv新注册一个文件（无其它文件干扰），4min内vod_push策略会下发sdk_download_task
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_multi_files_in_dir(file_count=1)
        wait_for_second(5 * 60)
        strategy_initialize_time = check_strategy_initialize_time()
        strategy_download_time = check_strategy_sdk_download_time()
        self.assertTrue(strategy_download_time - strategy_initialize_time <= 4 * 60 * 1000,
                        "strategy sdk_download_task issued not in time")

    @func_doc
    def testPushDistributeDownloadOneFile(self):
        """
        dir-srv新注册一个1GB，PPC=304的文件（无其它文件干扰），16min内seed文件全部下载完成
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=304)
        wait_for_second(20 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 855, "sdk_download_task num should be no more than 855")
        strategy_initialize_time = check_strategy_initialize_time()
        strategy_last_download_time = check_strategy_sdk_download_final_time()
        self.assertTrue(strategy_last_download_time - strategy_initialize_time <= 16 * 60 * 1000,
                        "strategy single_file push not in time")

    @func_doc
    def testPushDistributeDownloadTenFile(self):
        """
        dir-srv新注册10个1GB-20GB的文件，PPC从32-304不等（无其它文件干扰），3h内seed文件全部下载完成
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_multi_files_in_dir(file_count=10, ppc=None)
        wait_for_second(3.2 * 60 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 8550, "sdk_download_task num should be no more than 900")
        strategy_initialize_time = check_strategy_initialize_time()
        strategy_last_download_time = check_strategy_sdk_download_final_time() + 60000
        self.assertTrue(strategy_last_download_time - strategy_initialize_time <= 3 * 60 * 60 * 1000,
                        "push_distribute_time exceeds expected time ")

    @func_doc
    def testPushDistributePushDelete(self):
        """
        dir-srv删除已存在的文件（vod_push_srv已下载完成该文件），21min内vod_push策略会生成该文件的push_delete_task
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=304)
        wait_for_second(20 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 855, "sdk_download_task num should be no more than 855")
        del_file_in_dir()
        delete_file_dir_time = long(time.time() * 1000)
        wait_for_second(30 * 60)
        push_delete_time = check_strategy_push_delete_time()
        self.assertTrue(push_delete_time + 60 * 1000 - delete_file_dir_time <= 21 * 60 * 60 * 1000,
                        "strategy push_delete_task not in time")

    @func_doc
    def testPushDistributeSDKDelete(self):
        """
        dir-srv删除已存在的文件（SDK已下载完成该文件），21min内vod_push策略会生成该文件的sdk_delete_task
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_one_file_in_dir(file_size=1 * 1024 * 1024 * 1024, ppc=304)
        wait_for_second(20 * 60)
        del_file_in_dir()
        delete_file_dir_time = long(time.time() * 1000)
        wait_for_second(30 * 60)
        sdk_delete_time = check_strategy_sdk_delete_time()
        self.assertTrue(sdk_delete_time + 60 * 1000 - delete_file_dir_time <= 21 * 60 * 60 * 1000,
                        "strategy sdk_delete_task not in time")

    @func_doc
    def testPushDistributeDownloadHundredFile(self):
        """
        dir-srv新注册100个1GB-20GB的文件，PPC从32-304不等（无其它文件干扰），1天内seed文件全部下载完成
        """
        change_config(push_download_bandwidth=1000, seed_download_bandwidth=100, file_count=0, peer_count=0)
        start_vod_config()
        add_multi_files_in_dir(file_count=100, ppc=None)
        wait_for_second(36 * 60 * 60)
        self.assertTrue(check_sdk_download_task_num() <= 85500, "sdk_download_task num should be no more than 85500")
        strategy_initialize_time = check_strategy_initialize_time()
        strategy_last_download_time = check_strategy_sdk_download_final_time() + 60000
        self.assertTrue(strategy_last_download_time - strategy_initialize_time <= 35 * 60 * 60 * 1000,
                        "push_distribute_time exceeds expected time ")

if __name__ == '__main__':
    # 1、构造用例集
    suite = unittest.TestSuite()

    # 2、执行顺序是安加载顺序：先执行test_sub，再执行test_add
    suite.addTest(TestTimeliness("testPushDistributeDownloadTenFile"))
    # suite.addTest(TestTimeliness("test_add"))

    # 3、实例化runner类
    runner = unittest.TextTestRunner()

    # 4、执行测试
    runner.run(suite)
    # unittest.main()