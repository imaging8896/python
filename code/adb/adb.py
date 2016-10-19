import subprocess
from subprocess import Popen, PIPE
import os
import time
from datetime import datetime
import shutil


class ADB(object):

    def __init__(self, serial_num):
        self.serial_num = serial_num
        THIS_DIR = os.path.abspath(os.path.dirname(__file__))
        report_dir = os.path.join(THIS_DIR, "report")
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        self.log_file = os.path.join(report_dir, "ADB")
        self.check_availability()

    def is_available(self):
        out, err = self.exec_adb("devices")
        if "no devices" in err:
            return False
        if self.serial_num and self.serial_num not in out:
            return False
        return True

    def check_availability(self):
        if not self.is_available():
            raise Exception("Adb device not found.")

    def is_available_and_sys_ready_until(self, timeout):
        while not self.is_available() and timeout >= 0:
            time.sleep(10)
            timeout -= 10
        out, _ = self.exec_shell(
            "ls /sdcard/ | grep 'No such file or directory'")
        while out and timeout >= 0:
            time.sleep(10)
            out, _ = self.exec_shell(
                "ls /sdcard/ | grep 'No such file or directory'")
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
        if not self.is_available_and_sys_ready_until(timeout):
            raise Exception("Timeout when wait device bootup")

    def pull(self, src, dest):
        return self.exec_adb("pull {0} {1}".format(src, dest))

    def pull_as_root(self, src, dest):
        self.exec_shell(
            "su 0 cp {0} /storage/emulated/0/Download/".format(src))
        name = os.path.basename(src)
        out, err = self.pull("/storage/emulated/0/Download/" + name, dest)
        self.exec_shell("rm -f /storage/emulated/0/Download/{0}".format(name))
        return out, err

    def push(self, src, dest):
        return self.exec_adb("push {0} {1}".format(src, dest))

    def push_as_root(self, src, dest):
        self.push(src, "/data/local/tmp")
        name = os.path.basename(src)
        return self.exec_shell("su 0 mv /data/local/tmp/{0} {1}".format(name, dest))

    def install(self, apk):
        return self.exec_adb("install -g " + apk)

    def uninstall(self, package):
        return self.exec_adb("uninstall " + package)

    def get_logcat(self, path, tag=None):
        tag_opt = "-s " + tag if tag else ""
        self.exec_adb("logcat -d {0} | tee {1}".format(tag_opt, path))

    def logcat(self, tag=None):
        tag_opt = "-s " + tag if tag else ""
        return self.exec_adb("logcat -d {0}".format(tag_opt))

    def clear_logcat(self):
        return self.exec_adb("logcat -c")

    def reboot(self, timeout=240):
        self.exec_shell("svc power reboot")
        time.sleep(20)
        if not self.is_available_and_sys_ready_until(timeout):
            raise Exception("Timeout when wait device bootup")

    def reboot_async(self):
        cmd = self.__get_cmd_prefix() + " shell su 0 svc power reboot"
        Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

    def enable_wifi(self):
        return self.exec_shell("svc wifi enable")

    def disable_wifi(self):
        return self.exec_shell("svc wifi disable")

    def grant_permission(self, pkg, permission):
        return self.exec_shell("pm grant {0} {1}".format(pkg, permission))

    def exec_shell(self, cmd, shutup=True):
        return self.exec_adb("shell " + cmd, shutup)

    def exec_adb(self, cmd, shutup=True):
        with open(self.log_file, "a") as log_file:
            cmd = self.__get_cmd_prefix() + " " + cmd
            if shutup:
                process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                out, err = process.communicate()
            else:
                subprocess.call(cmd, shell=True)
                out, err = "", ""
            msg = "{0} : {1} : ({2},{3})\n".format(
                str(datetime.now()), cmd, out.rstrip(), err.rstrip())
            log_file.write(msg)
        return out, err

    def __get_cmd_prefix(self):
        return "adb {0}".format("-s " + self.serial_num if self.serial_num else "-d")

    def clear_log(self):
        report_dir = os.path.dirname(self.log_file)
        if os.path.exists(report_dir):
            shutil.rmtree(report_dir)
