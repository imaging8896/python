import subprocess
from subprocess import Popen, PIPE
import os
from os.path import abspath
from os.path import dirname
from os.path import basename
from os.path import exists as dirExists
from os.path import join as pathJoin
import time
from datetime import datetime


class ADB(object):

    def __init__(self, serial_num):
        self.serial_num = serial_num
        self.logger = Logger()
        self.report_dir = self.logger.report_dir
        self.check_availability()

    def is_available(self):
        out, err = self.exec_adb("devices")
        if "no devices" in err:
            return False
        if self.serial_num and self.serial_num not in out:
            return False
        return True

    def get_state(self):
        out, _ = self.exec_adb("get-state")
        return out.strip()

    def check_availability(self):
        if not self.is_available():
            raise Exception("Adb device not found.")

    def is_boot_completed(self):
        out, _ = self.exec_shell("getprop sys.boot_completed")
        return True if out.rstrip() == "1" else False

    def wait_boot_completed_until(self, timeout):
        while not self.is_available() and timeout >= 0:
            time.sleep(10)
            timeout -= 10
        while not self.is_boot_completed() and timeout >= 0:
            time.sleep(10)
            timeout -= 10
        return timeout >= 0

    def su_root(self):
        return self.exec_adb("root")

    def su_shell(self):
        return self.exec_shell("'setprop service.adb.root 0; setprop ctl.restart adbd'")

    def enable_verity(self):
        return self.exec_adb("enable-verity")

    def disable_verity(self):
        return self.exec_adb("disable-verity")

    def remount(self):
        return self.exec_adb("remount")

    def hard_reboot(self, timeout=240):
        self.exec_adb("reboot")
        time.sleep(20)
        if not self.wait_boot_completed_until(timeout):
            raise Exception("Timeout when wait device bootup")

    def pull(self, src, dest):
        return self.exec_adb("pull {0} {1}".format(src, dest))

    def pull_as_root(self, src, dest):
        self.exec_shell(
            "su 0 cp {0} /data/local/tmp".format(src))
        pull_src = "/data/local/tmp/" + basename(src)
        self.exec_shell("su 0 chmod 777 " + pull_src)
        out, err = self.pull(pull_src, dest)
        self.exec_shell("rm -f /data/local/tmp/{0}".format(basename(src)))
        return out, err

    def push(self, src, dest):
        return self.exec_adb("push {0} {1}".format(src, dest))

    def push_as_root(self, src, dest):
        self.push(src, "/data/local/tmp")
        name = basename(src)
        return self.exec_shell("su 0 mv /data/local/tmp/{0} {1}".format(name, dest))

    def install(self, apk):
        return self.exec_adb("install -g " + apk)

    def uninstall(self, package):
        return self.exec_adb("uninstall " + package)

    def get_logcat(self, path, tag=None):
        tag_opt = "-s " + tag if tag else ""
        self.exec_adb(
            "logcat -d {0} | tee {1}".format(tag_opt, path), not_log=True)

    def logcat(self, tag=None):
        tag_opt = "-s " + tag if tag else ""
        return self.exec_adb("logcat -d {0}".format(tag_opt), not_log=True)

    def clear_logcat(self):
        return self.exec_adb("logcat -c")

    def reboot(self, timeout=240):
        self.exec_shell("su 0 svc power reboot")
        time.sleep(20)
        if not self.wait_boot_completed_until(timeout):
            raise Exception("Timeout when wait device bootup")

    def reboot_async(self):
        cmd = self.__get_cmd_prefix() + " shell su 0 svc power reboot"
        Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

    def enable_wifi(self):
        return self.exec_shell("su 0 svc wifi enable")

    def disable_wifi(self):
        return self.exec_shell("su 0 svc wifi disable")

    def enable_4g(self):
        return self.exec_shell("su 0 svc data enable")

    def disable_4g(self):
        return self.exec_shell("su 0 svc data disable")

    def grant_permission(self, pkg, permission):
        # no su 0, this make 'root' grant permission to app not 'shell'
        return self.exec_shell("pm grant {0} {1}".format(pkg, permission))

    def exec_shell(self, cmd, silent=True, not_log=False):
        return self.exec_adb("shell " + cmd, silent)

    def exec_adb(self, cmd, silent=True, not_log=False):
        with open(self.logger.get_log_file(), "a") as log_file:
            cmd = self.__get_cmd_prefix() + " " + cmd
            if silent:
                process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                out, err = process.communicate()
            else:
                subprocess.check_output(cmd, shell=True)
                out, err = "", ""
            if not not_log:
                msg = "{0} : {1} : ({2},{3})\n".format(
                    str(datetime.now()), cmd, out.rstrip(), err.rstrip())
                log_file.write(msg)
        return out, err

    def get_dmesg(self, path):
        self.exec_shell("dmesg > " + path, not_log=True)

    def get_version(self):
        out, _ = self.exec_shell("getprop ro.build.version.incremental")
        return int(out.rstrip())

    def get_logs(self, logcat_tag=["HopeBay", "TeraService"]):
        version = self.get_version()
        logs_dir = pathJoin(self.report_dir, get_new_dirname(version))
        if not dirExists(logs_dir):
            os.makedirs(logs_dir)
        self.get_tombstones(logs_dir)
        self.get_hcfs_bin(logs_dir)
        self.get_hcfs_log(logs_dir)
        for tag in logcat_tag:
            self.get_logcat(pathJoin(logs_dir, tag + "_logcat"), tag)
        self.get_logcat(pathJoin(logs_dir, "logcat"))
        self.get_dmesg(pathJoin(logs_dir, "dmesg"))
        return logs_dir

    def get_hcfs_log(self, path):
        self.pull("/data/hcfs_android_log", path)
        # self.pull("/data/hcfs_android_log.1", path)
        # self.pull("/data/hcfs_android_log.2", path)
        # self.pull("/data/hcfs_android_log.3", path)
        # self.pull("/data/hcfs_android_log.4", path)
        # self.pull("/data/hcfs_android_log.5", path)

    def get_hcfs_bin(self, path):
        self.pull_as_root("/system/bin/hcfs", path)

    def get_tombstones(self, path):
        out, _ = self.exec_shell("su 0 ls -l /data/tombstones/")
        # -rw------- system   system     491314 2016-12-09 09:56 tombstone_09
        for line in out.rstrip().split("\r\n"):
            _, _, _, _, day, time, tombstone = filter(None, line.split(" "))
            dest = pathJoin(path, day + "-" + time + "-" + tombstone)
            self.pull_as_root("/data/tombstones/" + tombstone, dest)

    def __get_cmd_prefix(self):
        return "adb {0}".format("-s " + self.serial_num if self.serial_num else "-d")


class Logger(object):

    def __init__(self):
        self.report_dir = pathJoin(abspath(dirname(__file__)), "adb_log")
        if not dirExists(self.report_dir):
            os.makedirs(self.report_dir)

    def get_log_file(self):
        if not dirExists(self.report_dir):
            os.makedirs(self.report_dir)
        return pathJoin(self.report_dir, "ADB")


def get_new_dirname(version):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    return "{0}-{1}".format(str(version), timestamp)
