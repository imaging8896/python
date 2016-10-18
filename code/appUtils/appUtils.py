from os.path import isfile as fileExist
from os.path import join as pathJoin
import xunitparser

from ..adb.factory import *
from ..adb.activityManager import InstrumentBuilder
import config
from app import BaseApp

logger = config.get_logger().getChild(__file__)
TEST_RUNNER = "com.zutubi.android.junitreport.JUnitReportTestRunner"


def run_release_app_instrument_test(app, instrument_builder, report_path):
    check_if_valid_app(app)
    check_if_valid_instrument_builder(instrument_builder)

    app.build_clean()
    app.build_release()
    app.uninstall()
    app.install()
    app.acquire_permissions()
    instrument_builder.add_test_runner(app.package + "/" + TEST_RUNNER)
    am.run_instrument(instrument_builder)
    app.get_report(report_path)
    app.uninstall()
    app.clear_apk()


###################### private #########################

def check_if_valid_app(test_obj):
    if not issubclass(type(test_obj), BaseApp):
        raise ValueError("Argument should be sub class of 'app.BaseApp'")


def check_if_valid_instrument_builder(test_obj):
    if not isinstance(test_obj, InstrumentBuilder):
        raise ValueError(
            "Argument should be instance of 'activityManager.InstrumentBuilder'")


def check_if_test_success(app, report, method=None):
    report_file_path = pathJoin(self.REPORT_DIR, self.REPORT_FILE_NAME)
    if not fileExist(report):
        raise Exception("Junit report file not found")
    with open(report_file_path) as report_file:
        test_suite, test_result = xunitparser.parse(report_file)
        for test_case in test_suite:
            logger.info("Class <{0}>, method<{1}>".format(
                test_case.classname, test_case.methodname))
            if not test_case.good:
                raise Exception(test_case.alltext)
            if test_case.classname != app.package + "." + app.clazz or (method and test_case.methodname != method):
                raise Exception("Test result not found.")
