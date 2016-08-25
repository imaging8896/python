import subprocess
from subprocess import Popen, PIPE
import os
import time

import config

logger = config.get_logger().getChild(__name__)


def isAvailable(serialno=""):
    logger.info("Check if phone <" + serialno + "> is adb available.")
    if serialno:
        cmd = "adb get-serialno | grep " + serialno
        pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = pipe.communicate()
        logger.debug("isAvailable" + repr((cmd, out, err)))
        return True if out else False
    else:
        cmd = "adb get-serialno | grep unknown"
        pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = pipe.communicate()
        logger.debug("isAvailable" + repr((cmd, out, err)))
        return False if out else True


def isAvailable_and_sys_ready_until(timeout, serialno=""):
    while not isAvailable(serialno) and timeout >= 0:
        time.sleep(10)
        timeout -= 10
    while not is_file_available("/sdcard/") and timeout >= 0:
        time.sleep(10)
        timeout -= 10
    return timeout >= 0


def pull(src, dest, serialno=""):
    logger.info("Pull file from phone <" + serialno + ">.")
    assert is_file_available(src, serialno), "No such file or dir"
    cmd = __get_cmd_prefix(serialno) + " pull " + src + " " + dest
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pipe.communicate()
    logger.debug("pull" + repr((cmd, out, err)))


def push_as_root(src, dest, name, serialno=""):
    push(src, "/data/local/tmp", serialno)
    cmd = "mv /data/local/tmp/" + name + " " + dest
    out, err = exec_cmd(cmd, serialno)
    logger.debug("push_as_root" + repr((cmd, out, err)))
    assert not err, err


def push(src, dest, serialno=""):
    logger.info("Push file to phone <" + serialno + ">.")
    cmd = __get_cmd_prefix(serialno) + " push " + src + " " + dest
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pipe.communicate()
    logger.debug("push" + repr((cmd, out, err)))
    assert not err, err


def get_logcat(path, tag="HopeBay", serialno=""):
    cmd = __get_cmd_prefix(serialno) + " logcat -d -s " + tag
    cmd = cmd + " | tee " + path
    subprocess.call(cmd, shell=True, stdout=PIPE, stderr=PIPE)


def exec_cmd(cmd, serialno=""):
    prefix = __get_cmd_prefix(serialno) + " shell su 0 "
    pipe = subprocess.Popen(prefix + cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pipe.communicate()
    logger.debug("exec_cmd" + repr((cmd, out, err)))
    return out, err


def get_file(name, src, dest, serialno=""):
    cmd = "cp " + src + " /sdcard/Download/"
    exec_cmd(cmd, serialno)
    # cmd = "cat  /data/local/tmp/" + name + " > " + dest
    # exec_cmd(cmd)
    pull("/sdcard/Download/" + name, dest)
    rm_file("/sdcard/Download/" + name)


def get_hcfs_log(path):
    get_file("hcfs_android_log", "/data/hcfs_android_log", path)


def get_file_size(path, serialno=""):
    cmd = "stat -c%s" + path
    return exec_cmd(cmd, serialno)


def reboot(timeout=120, serialno=""):
    cmd = "reboot"
    out, err = exec_cmd(cmd, serialno)
    assert not out and not err, "Should not output anything."
    time.sleep(60)
    assert isAvailable_and_sys_ready_until(
        timeout, serialno), "Timeout when wait device bootup"


def gen_dir(path, serialno=""):
    cmd = "mkdir " + path
    out, err = exec_cmd(cmd, serialno)
    assert not out and not err, repr((out, err))


# Remove recursively when path target is a directory


def rm_file(path, serialno=""):
    cmd = "rm -rf " + path
    out, err = exec_cmd(cmd, serialno)


def enable_wifi(serialno=""):
    return exec_cmd("svc wifi enable", serialno)


def disable_wifi(serialno=""):
    return exec_cmd("svc wifi disable", serialno)


def start_app(pkg, activity, serialno=""):
    cmd = "am start  " + pkg + "/." + activity
    return exec_cmd(cmd, serialno)


def is_file_available(path, serialno=""):
    cmd = "ls " + path + " | grep 'No such file or directory'"
    out, err = exec_cmd(cmd, serialno)
    return True if not out else False

# adb wait-for-device shell ...
# adb wait-for-device


def __get_cmd_prefix(serialno=""):
    cmd_list = ["adb"]
    cmd_list.extend(["-s", serialno] if serialno else [])
    return " ".join(cmd_list)
