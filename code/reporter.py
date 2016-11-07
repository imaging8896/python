import os
from os import makedirs
from os.path import isfile
from os.path import isdir
from os.path import join as pathJoin
from os.path import basename
from datetime import datetime
from shutil import move
from shutil import rmtree

from adb.factory import adb

# TODO get test device information


class Reporter(object):

    def __init__(self, log_save_dir):
        self.addition_log = []
        timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        tera_version = get_tera_version()
        dir_name = "{0}-{1}".format(str(tera_version), timestamp)
        self.log_save_dir = pathJoin(log_save_dir, dir_name)
        os.makedirs(self.log_save_dir)

    def add_log(self, log):
        self.addition_log += [log]

    def get_logs(self):
        get_hcfs_log(pathJoin(self.log_save_dir, "hcfs_android_log"))
        get_logcat(pathJoin(self.log_save_dir, "API_logcat"), "API")
        get_logcat(pathJoin(self.log_save_dir, "HB_logcat"), "HopeBay")
        get_logcat(pathJoin(self.log_save_dir, "logcat"))
        get_dmesg(pathJoin(self.log_save_dir, "dmesg"))

        for i, log in enumerate(self.addition_log):
            if isfile(log):
                log_name = basename(log) + str(i)
                move(log, pathJoin(self.log_save_dir, log_name))
            elif isdir(log):
                log_dest = pathJoin(self.log_save_dir, basename(log) + str(i))
                makedirs(log_dest)
                for file_name in os.listdir(log):
                    file = pathJoin(log, file_name)
                    move(file, pathJoin(log_dest, file_name))
                rmtree(log)
            else:
                raise Exception("log file neither file nor directory")


def get_tera_version():
    out, _ = adb.exec_shell("getprop ro.build.version.incremental")
    return int(out.rstrip())


def get_hcfs_log(path):
    adb.pull_as_root("/data/hcfs_android_log", path)


def get_logcat(path, tag=None):
    adb.get_logcat(path, tag)


def get_dmesg(path):
    adb.exec_shell("dmesg > " + path, not_log=True)
