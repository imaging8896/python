import subprocess
from subprocess import Popen, PIPE
import os
import time


def is_available(serial_num=None):
    cmd = "adb get-serialno"
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    if "no devices" in err:
        return False
    if serial_num and serial_num not in out:
        return False
    return True


def check_availability(serial_num=None):
    if not is_available():
        raise Exception("Adb device not found.")


def is_available_and_sys_ready_until(timeout, serial_num=None):
    while not is_available(serial_num) and timeout >= 0:
        time.sleep(10)
        timeout -= 10
    while not is_file_available("/sdcard/") and timeout >= 0:
        time.sleep(10)
        timeout -= 10
    return timeout >= 0


def pull(src, dest, serial_num=None):
    if not is_file_available(src, serial_num):
        raise Exception("No such file or dir")
    cmd = __get_cmd_prefix(serial_num)
    cmd += " pull {0} {1}".format(src, dest)
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def install(apk_path, serial_num=None):
    cmd = __get_cmd_prefix(serial_num) + " install -g " + apk_path
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def uninstall(package, serial_num=None):
    cmd = __get_cmd_prefix(serial_num) + " uninstall " + package
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def push_as_root(src, dest, name=None, serial_num=None):
    push(src, "/data/local/tmp", serial_num)
    if not name:
        name = src.split("/")[-1]
    cmd = "mv /data/local/tmp/" + name + " " + dest
    return exec_cmd(cmd, serial_num)


def push(src, dest, serial_num=None):
    cmd = __get_cmd_prefix(serial_num)
    cmd += " push {0} {1}".format(src, dest)
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def get_logcat(path, tag="HopeBay", serial_num=None):
    cmd = __get_cmd_prefix(serial_num)
    cmd += " logcat -d -s {0} | tee {1}".format(tag, path)
    subprocess.call(cmd, shell=True, stdout=PIPE, stderr=PIPE)


def exec_cmd(cmd, serial_num=None):
    prefix = __get_cmd_prefix(serial_num) + " shell su 0 "
    process = Popen(prefix + cmd, shell=True, stdout=PIPE, stderr=PIPE)
    return process.communicate()


def get_file(src, dest, name=None, serial_num=None):
    if not name:
        name = src.split("/")[-1]
    cmd = "cp " + src + " /storage/emulated/0/Download/"
    exec_cmd(cmd, serial_num)
    out, err = pull("/storage/emulated/0/Download/" + name, dest)
    rm_file("/storage/emulated/0/Download/" + name)
    return out, err


def get_hcfs_log(path):
    return get_file("/data/hcfs_android_log", path)


def get_file_size(path, serial_num=None):
    cmd = "stat -c%s" + path
    return exec_cmd(cmd, serial_num)


def reboot(timeout=240, serial_num=None):
    exec_cmd("svc power reboot")
    time.sleep(20)
    if not is_available_and_sys_ready_until(timeout, serial_num):
        raise Exception("Timeout when wait device bootup")


def reboot_async(serial_num=None):
    cmd = __get_cmd_prefix(serial_num) + " shell su 0 svc power reboot"
    Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)


def gen_dir(path, serial_num=None):
    cmd = "mkdir " + path
    return exec_cmd(cmd, serial_num)


def rm_file(path, serial_num=None):
    cmd = "rm -rf " + path
    return exec_cmd(cmd, serial_num)


def enable_wifi(serial_num=None):
    return exec_cmd("svc wifi enable", serial_num)


def disable_wifi(serial_num=None):
    return exec_cmd("svc wifi disable", serial_num)


def start_app(pkg, activity, serial_num=None):
    cmd = "am start {0}/.{1}".format(pkg, activity)
    return exec_cmd(cmd, serial_num)


def is_file_available(path, serial_num=None):
    cmd = "ls " + path + " | grep 'No such file or directory'"
    out, err = exec_cmd(cmd, serial_num)
    return True if not out else False


def __get_cmd_prefix(serial_num=None):
    return "adb {0}".format("-s" + serial_num if serial_num else "")


class ADBWrapper(object):

    def __init__(self, serial_num=None):
        self.serial_num = serial_num

    def exec_cmd(self, cmd):
        return exec_cmd(cmd, self.serial_num)
