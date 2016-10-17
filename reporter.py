import os
from datetime import datetime
from shutil import copyfile

from adb.factory import adb


class Reporter(object):

    def __init__(self, log_save_dir):
        self.addition_log = []
        self.log_save_dir = log_save_dir
        if not os.path.exists(self.log_save_dir):
            os.makedirs(self.log_save_dir)

    def add_log(self, log):
        self.addition_log = [log]

    def get_logs(self):
        suffix = datetime.now().strftime("%M%S%f")
        hcfs_android_log = os.path.join(self.log_save_dir, "hcfs_android_log-")
        adb.pull_as_root("/data/hcfs_android_log", hcfs_android_log + suffix)
        logcat = os.path.join(self.log_save_dir, "logcat-")
        adb.get_logcat(logcat + suffix)
        dmesg = os.path.join(self.log_save_dir, "dmesg-")
        adb.exec_shell("dmesg > " + dmesg + suffix)

        for i, log in enumerate(self.addition_log):
            log_name = os.path.basename(log) + str(i)
            log_dest = os.path.join(self.log_save_dir, log_name + "-")
            copyfile(log, log_dest + suffix)
