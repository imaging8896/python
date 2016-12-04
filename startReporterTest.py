'''
Created on 2016.10.16

@author: chen
'''

from os import listdir
from os import makedirs
from os.path import abspath
from os.path import dirname
from os.path import basename
from os.path import join as pathJoin
from os.path import exists as dirExists
from os.path import isfile as fileExists
from shutil import rmtree
import unittest

from code.reporter import Reporter
from code.adb.factory import adb


class GetLogPlusHCFSLogsTestCase(unittest.TestCase):
    def setUp(self):
        this_dir = abspath(dirname(__file__))
        self.log_save_dir = pathJoin(this_dir, "test1")
        self.log_dir = pathJoin(this_dir, "abc")
        makedirs(self.log_dir)
        self.log_files = [pathJoin(self.log_dir, "f1")]
        self.log_files += [pathJoin(self.log_dir, "f2")]
        self.log_files += [pathJoin(self.log_dir, "f3")]
        for file in self.log_files:
            open(file, "a").close()
        self.reporter = Reporter(self.log_save_dir)
        self.reporter.add_log(self.log_dir)
        self.hcfs_logs_dir = pathJoin(
            basename(adb.report_dir), basename(adb.get_logs()))
        self.reporter.add_log(adb.report_dir)

    def tearDown(self):
        self.assertFalse(dirExists(self.log_dir))
        rmtree(self.log_save_dir)

    def test_get_log_first_time(self):
        self.reporter.get_logs()

        latest_dir = pathJoin(self.log_save_dir, "latest")
        sub_latest_dir = [pathJoin(latest_dir, x) for x in listdir(latest_dir)]
        self.assertEqual(1, len(sub_latest_dir))
        final_dir = sub_latest_dir[0]
        final_log_dir = pathJoin(final_dir, "abc")
        hcfs_log_dir = pathJoin(final_dir, self.hcfs_logs_dir)
        adb_log_dir = pathJoin(hcfs_log_dir, "..")
        final_log_files = [pathJoin(final_log_dir, "f1")]
        final_log_files += [pathJoin(final_log_dir, "f2")]
        final_log_files += [pathJoin(final_log_dir, "f3")]
        final_log_files += [pathJoin(hcfs_log_dir, "hcfs_android_log")]
        final_log_files += [pathJoin(hcfs_log_dir, "API_logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "HopeBay_logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "TeraService_logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "dmesg")]
        final_log_files += [pathJoin(adb_log_dir, "ADB")]
        self.assertTrue(dirExists(final_log_dir))
        self.assertTrue(all(map(fileExists, final_log_files)), str(
            map(fileExists, final_log_files)) + ":" + str(final_log_files))

    def test_get_log_old_log(self):
        self.reporter.get_logs()
        makedirs(self.log_dir)
        for file in self.log_files:
            open(file, "a").close()
        new_reporter = Reporter(self.log_save_dir)
        new_reporter.add_log(self.log_dir)
        adb.get_logs()
        new_reporter.add_log(adb.report_dir)
        new_reporter.get_logs()

        old_full_logs = [pathJoin(self.log_save_dir, x)
                         for x in listdir(self.log_save_dir) if x != "latest"]
        self.assertEqual(1, len(old_full_logs))
        old_full_log_dir = old_full_logs[0]
        log_dir = pathJoin(old_full_log_dir, "abc")
        hcfs_log_dir = pathJoin(old_full_log_dir, self.hcfs_logs_dir)
        adb_log_dir = pathJoin(hcfs_log_dir, "..")
        log_files = [pathJoin(log_dir, "f1")]
        log_files += [pathJoin(log_dir, "f2")]
        log_files += [pathJoin(log_dir, "f3")]
        log_files += [pathJoin(hcfs_log_dir, "hcfs_android_log")]
        log_files += [pathJoin(hcfs_log_dir, "API_logcat")]
        log_files += [pathJoin(hcfs_log_dir, "HopeBay_logcat")]
        log_files += [pathJoin(hcfs_log_dir, "TeraService_logcat")]
        log_files += [pathJoin(hcfs_log_dir, "logcat")]
        log_files += [pathJoin(hcfs_log_dir, "dmesg")]
        log_files += [pathJoin(adb_log_dir, "ADB")]
        self.assertTrue(dirExists(log_dir))
        self.assertTrue(all(map(fileExists, log_files)), str(
            map(fileExists, log_files)) + ":" + str(log_files))

    def test_get_log_not_first_time(self):
        self.reporter.get_logs()
        makedirs(self.log_dir)
        for file in self.log_files:
            open(file, "a").close()
        new_reporter = Reporter(self.log_save_dir)
        new_reporter.add_log(self.log_dir)
        self.hcfs_logs_dir = pathJoin(
            basename(adb.report_dir), basename(adb.get_logs()))
        new_reporter.add_log(adb.report_dir)
        new_reporter.get_logs()

        latest_dir = pathJoin(self.log_save_dir, "latest")
        sub_latest_dir = [pathJoin(latest_dir, x) for x in listdir(latest_dir)]
        self.assertEqual(1, len(sub_latest_dir))
        final_dir = sub_latest_dir[0]
        final_log_dir = pathJoin(final_dir, "abc")
        hcfs_log_dir = pathJoin(final_dir, self.hcfs_logs_dir)
        adb_log_dir = pathJoin(hcfs_log_dir, "..")
        final_log_files = [pathJoin(final_log_dir, "f1")]
        final_log_files += [pathJoin(final_log_dir, "f2")]
        final_log_files += [pathJoin(final_log_dir, "f3")]
        final_log_files += [pathJoin(hcfs_log_dir, "hcfs_android_log")]
        final_log_files += [pathJoin(hcfs_log_dir, "API_logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "HopeBay_logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "TeraService_logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "logcat")]
        final_log_files += [pathJoin(hcfs_log_dir, "dmesg")]
        final_log_files += [pathJoin(adb_log_dir, "ADB")]
        self.assertTrue(dirExists(final_log_dir))
        self.assertTrue(all(map(fileExists, final_log_files)), str(
            map(fileExists, final_log_files)) + ":" + str(final_log_files))


class GetLogTestCase(unittest.TestCase):
    def setUp(self):
        this_dir = abspath(dirname(__file__))
        self.log_save_dir = pathJoin(this_dir, "test1")
        self.log_dir = pathJoin(this_dir, "abc")
        makedirs(self.log_dir)
        self.log_files = [pathJoin(self.log_dir, "f1")]
        self.log_files += [pathJoin(self.log_dir, "f2")]
        self.log_files += [pathJoin(self.log_dir, "f3")]
        for file in self.log_files:
            open(file, "a").close()
        self.reporter = Reporter(self.log_save_dir)
        self.reporter.add_log(self.log_dir)

    def tearDown(self):
        self.assertFalse(dirExists(self.log_dir))
        rmtree(self.log_save_dir)

    def test_get_log_first_time(self):
        self.reporter.get_logs()

        latest_dir = pathJoin(self.log_save_dir, "latest")
        sub_latest_dir = [pathJoin(latest_dir, x) for x in listdir(latest_dir)]
        self.assertEqual(1, len(sub_latest_dir))
        final_dir = sub_latest_dir[0]
        final_log_dir = pathJoin(final_dir, "abc")
        final_log_files = [pathJoin(final_log_dir, "f1")]
        final_log_files += [pathJoin(final_log_dir, "f2")]
        final_log_files += [pathJoin(final_log_dir, "f3")]
        self.assertTrue(dirExists(final_log_dir))
        self.assertTrue(all(map(fileExists, final_log_files)), str(
            map(fileExists, final_log_files)) + ":" + str(final_log_files))

    def test_get_log_old_log(self):
        self.reporter.get_logs()
        makedirs(self.log_dir)
        for file in self.log_files:
            open(file, "a").close()
        new_reporter = Reporter(self.log_save_dir)
        new_reporter.add_log(self.log_dir)
        new_reporter.get_logs()

        old_full_logs = [pathJoin(self.log_save_dir, x)
                         for x in listdir(self.log_save_dir) if x != "latest"]
        self.assertEqual(1, len(old_full_logs))
        old_full_log_dir = old_full_logs[0]
        log_dir = pathJoin(old_full_log_dir, "abc")
        log_files = [pathJoin(log_dir, "f1")]
        log_files += [pathJoin(log_dir, "f2")]
        log_files += [pathJoin(log_dir, "f3")]
        self.assertTrue(dirExists(log_dir))
        self.assertTrue(all(map(fileExists, log_files)), str(
            map(fileExists, log_files)) + ":" + str(log_files))

    def test_get_log_not_first_time(self):
        self.reporter.get_logs()
        makedirs(self.log_dir)
        for file in self.log_files:
            open(file, "a").close()
        new_reporter = Reporter(self.log_save_dir)
        new_reporter.add_log(self.log_dir)
        new_reporter.get_logs()

        latest_dir = pathJoin(self.log_save_dir, "latest")
        sub_latest_dir = [pathJoin(latest_dir, x) for x in listdir(latest_dir)]
        self.assertEqual(1, len(sub_latest_dir))
        final_dir = sub_latest_dir[0]
        final_log_dir = pathJoin(final_dir, "abc")
        final_log_files = [pathJoin(final_log_dir, "f1")]
        final_log_files += [pathJoin(final_log_dir, "f2")]
        final_log_files += [pathJoin(final_log_dir, "f3")]
        self.assertTrue(dirExists(final_log_dir))
        self.assertTrue(all(map(fileExists, final_log_files)), str(
            map(fileExists, final_log_files)) + ":" + str(final_log_files))


if __name__ == '__main__':
    tests = ["test_get_log_first_time",
             "test_get_log_old_log", "test_get_log_not_first_time"]
    suite = unittest.TestSuite()
    suite.addTests(map(GetLogPlusHCFSLogsTestCase, tests))
    suite.addTests(map(GetLogTestCase, tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
