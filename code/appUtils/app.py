from os.path import join as pathJoin
from os.path import isfile as fileExist
from os.path import exists as dirExist
from os.path import abspath
from os.path import dirname
from os import makedirs
from os import remove

from ..adb.factory import *
from ..dockerBuildUtils import dockerBuildUtils

TEST_RUNNER = "com.zutubi.android.junitreport.JUnitReportTestRunner"


class BaseApp(object):

    def __init__(self, proj, package):
        self.PROJ_DIR = proj
        self.package = package
        self.app_path = pathJoin("/data", "data", self.package)
        self.apk = pathJoin(abspath(dirname(__file__)), "app.apk")
        dockerBuildUtils.gradle_build(self.PROJ_DIR, self.apk)

    def uninstall(self):
        out, err = adb.uninstall(self.package)
        if android_fileUtils.is_existed(self.app_path):
            raise Exception("Fail to uninstall app:" + str((out, err)))

    def install(self):
        out, err = adb.install(self.apk)
        if not android_fileUtils.is_existed(self.app_path):
            raise Exception("Fail to install apk:" + str((out, err)))

    def add_report(self, report_name):
        self.report_src = pathJoin(self.app_path, "files", report_name)

    def grant_permission(self, permission):
        adb.grant_permission(self.package, permission)

    def get_report(self, path):
        if not self.report_src:
            raise Exception("Un-set report file.")
        report_dir = dirname(path)
        if not dirExist(report_dir):
            makedirs(report_dir)
        adb.pull_as_root(self.report_src, path)

    def get_test_runner(self):
        return self.package + "/" + TEST_RUNNER

    def cleanup(self):
        if self.apk and fileExist(self.apk):
            remove(self.apk)

    def __str__(self):
        return "project({0}) package({1})".format(self.PROJ_DIR, self.package)
