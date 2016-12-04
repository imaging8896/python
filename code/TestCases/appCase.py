import xunitparser
from os.path import basename
from os.path import abspath
from os.path import dirname
from os.path import join as pathJoin
from os.path import exists as dirExists

from TestFramework import *
from Utils import config
from Utils import gradleUtils


def get_report_dir():
    import os
    report_dir = pathJoin(abspath(dirname(__file__)), "report")
    if not dirExists(report_dir):
        os.makedirs(report_dir)
    return report_dir


class JunitTestAppCase(Case):

    def __init__(self, proj_dir, report_path):
        self.logger = config.get_logger().getChild(
            __name__ + "." + self.__class__.__name__)
        self.proj_dir = proj_dir
        self.report_src = report_path
        self.test_args = []

    def setUp(self):
        pass

    def test(self):
        gradleUtils.exec_task("cC", self.proj_dir, self.test_args)
        self.get_report()
        _, test_result = self.parse_report()
        if not test_result.wasSuccessful():
            msg = ""
            for test_case, trace in test_result.errors:
                msg += "{0}\n{1}\n".format(str(test_case), trace)
                msg += "----------------------------------------------------\n"
            for test_case, trace in test_result.failures:
                msg += "{0}\n{1}\n".format(str(test_case), trace)
                msg += "----------------------------------------------------\n"
            raise TestAssertionError(msg)

    def tearDown(self):
        pass

    def test_package(self, package):
        self.logger.info("test_package " + package)
        key = "android.testInstrumentationRunnerArguments.package"
        self.test_args = ["-P{0}={1}".format(key, package)]
        return self

    def test_classes(self, classes):
        self.logger.info("test_classes " + str(classes))
        key = "android.testInstrumentationRunnerArguments.class"
        self.test_args = ["-P{0}={1}".format(key, classes)]
        return self

    def test_methods(self, methods):
        self.logger.info("test_methods " + str(methods))
        key = "android.testInstrumentationRunnerArguments.class"
        self.test_args = ["-P{0}={1}".format(key, methods)]
        return self

    def get_report(self):
        from datetime import datetime
        from shutil import move
        report_name = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        report_file_name = report_name + ".xml"
        self.report_dst = pathJoin(get_report_dir(), report_file_name)
        move(self.report_src, self.report_dst)

    def parse_report(self):
        self.logger.info("parse_report " + self.report_dst)
        with open(self.report_dst, "r") as report:
            return xunitparser.parse(report)

    def __str__(self):
        return "test({0}) app<{1}>".format(type(self).__name__, str(basename(self.proj_dir)))
