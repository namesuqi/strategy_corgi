#!/usr/bin/python
# coding=utf-8
# corgi main test_case
# __author__ = 'JinYiFan'

import HTMLTestRunner
from testsuite.strategy_algorithm.algorithm_correctness import *
from testsuite.strategy_algorithm.algorithm_robustness import *
from testsuite.strategy_algorithm.algorithm_timeliness import *

if __name__ == '__main__':
    # os.system("python -m unittest -v testsuite.push.push_distribute")
    suitetest = unittest.TestSuite()
    suitetest.addTest(TestTimeliness("testPushDistributeDownloadHundredFile"))
    runner = unittest.TextTestRunner()
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    # report storage path
    # filename = 'E:\\git\corgi\\test_report\\report_{0}.html'.format(now)
    filename = REPORT_PATH + "/main.html"

    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(fp, title=u'strategy', description=u'This is a strategy_report test')
    runner.run(suitetest)
    fp.close()

# --------------------------------------
# suite = unittest.TestSuite()
# suite.addTest(Test("test_add2"))
# suite.addTest(Test("test_add1"))

# runner = unittest.TextTestRunner()
# runner.run(suite)

# ------------------------------------------------
# test_dir = './'
# discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')

# runner = unittest.TextTestRunner()
# runner.run(discover)

# ------------------------------------------------
# unittest.main()
