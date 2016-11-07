import xunitparser
import os
from os.path import abspath
from os.path import dirname
from os.path import join as pathJoin
from os.path import exists as dirExists

from TestFramework import *
from Utils import config
from Utils.adb.factory import adb, am
from Utils.adb.activityManager import InstrumentBuilder


def get_report_dir():
    report_dir = pathJoin(abspath(dirname(__file__)), "report")
    if not dirExists(report_dir):
        os.makedirs(report_dir)
    return report_dir


class JunitTestAppCase(Case):
    REPORT_NAME = "report.xml"

    def __init__(self, test_app):
        self.logger = config.get_logger().getChild(
            __name__ + "." + self.__class__.__name__)
        self.instrument_builder = InstrumentBuilder()
        self.instrument_builder.add_report(self.REPORT_NAME)
        self.app = test_app
        self.app.add_report(self.REPORT_NAME)
        self.test_package = None
        self.test_classes = None
        self.test_methods = None

    def setUp(self):
        self.logger.info("Setup")
        self.logger.info("setenforce 0")
        adb.exec_shell("su 0 setenforce 0")
        self.logger.info("uninstall app")
        self.app.uninstall()
        self.logger.info("install app")
        self.app.install()
        self.logger.info("acquire permissions for app")
        self.acquire_permissions()

    def test(self):
        self.instrument_builder.add_test_runner(self.app.get_test_runner())
        am.run_instrument(self.instrument_builder)
        self.get_report()

        test_suite, test_result = self.parse_report()
        msg = "Errors={0}, failures={1}".format(
            test_result.errors, test_result.failures)
        assert_true(test_result.wasSuccessful(), msg)

    def tearDown(self):
        self.logger.info("Teardown")
        self.logger.info("setenforce 1")
        adb.exec_shell("su 0 setenforce 1")
        self.logger.info("uninstall app")
        self.app.uninstall()

    def acquire_permissions(self):
        pass

    def set_test_package(self, package):
        self.logger.info("set_test_package " + package)
        self.test_package = package
        self.instrument_builder.add_scope_package(package)

    def set_test_classes(self, classes):
        self.logger.info("set_test_classes " + str(classes))
        self.test_classes = classes
        self.instrument_builder.add_scope_class(",".join(classes))

    def set_test_methods(self, methods):
        self.logger.info("set_test_methods " + str(methods))
        self.test_methods = methods
        self.instrument_builder.add_scope_method(",".join(methods))

    def get_report(self):
        from datetime import datetime
        report_name = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        report_file_name = report_name + ".xml"
        self.REPORT_PATH = pathJoin(get_report_dir(), report_file_name)
        self.app.get_report(self.REPORT_PATH)

    def parse_report(self):
        self.logger.info("parse_report " + self.REPORT_PATH)
        with open(self.REPORT_PATH, "r") as report:
            return xunitparser.parse(report)

    def __str__(self):
        return "test({0}) app<{1}>".format(type(self).__name__, str(self.app))
