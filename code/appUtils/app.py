from os.path import join as pathJoin
from os.path import isfile as fileExist
from os.path import exists as dirExist
from os.path import abspath
from os.path import dirname
from os import makedirs
from os import remove

from ..adb.factory import *
from ..dockerBuildUtils import dockerBuildUtils
import config

THIS_DIR = abspath(dirname(__file__))
APK = pathJoin(THIS_DIR, "app.apk")


class BaseApp(object):

    def __init__(self, proj, package):

        self.PROJ_DIR = proj

        self.logger = config.get_logger().getChild(self.__class__.__name__)
        self.package = package
        self.app_path = pathJoin("/data", "data", self.package)
        self.apk = None

    def build_clean(self):
        self.logger.info("build_clean")
        self.clear_apk()

    def build_release(self):
        self.logger.info("build_release")
        self.apk = APK
        dockerBuildUtils.gradle_build(self.PROJ_DIR, self.apk)

    def uninstall(self):
        self.logger.info("uninstall")
        out, err = adb.uninstall(self.package)
        if android_fileUtils.is_existed(self.app_path):
            raise Exception("Fail to uninstall app:" + str((out, err)))

    def install(self):
        self.logger.info("install")
        if not self.apk:
            raise Exception("Should be build before install")
        out, err = adb.install(self.apk)
        if not android_fileUtils.is_existed(self.app_path):
            raise Exception("Fail to install apk:" + str((out, err)))

    def add_report(self, report_name):
        self.logger.info("add_report " + report_name)
        self.report_src = pathJoin(self.app_path, "files", report_name)

    def acquire_permissions(self):
        pass

    def grant_permission(self, permission):
        self.logger.info("acquire_permissions '{0}' '{1}'".format(
            self.package, permission))
        adb.grant_permission(self.package, permission)

    def get_report(self, path):
        self.logger.info("get_report " + path)
        if not self.report_src:
            raise Exception("Un-set report file.")
        report_dir = dirname(path)
        if not dirExist(report_dir):
            makedirs(report_dir)
        adb.pull_as_root(self.report_src, path)

    def clear_apk(self):
        if self.apk and fileExist(self.apk):
            remove(self.apk)
            self.apk = None
