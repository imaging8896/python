import os
import subprocess
from subprocess import Popen, PIPE
import json

import makeUtils
import config
from ..adb.factory import *

logger = config.get_logger().getChild(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

HCFS_LIB_PHONE_PATH = "/system/lib64/libHCFS_api.so"
HCFS_LIB = THIS_DIR + "/libHCFS_api.so"

ADAPTER_NAME = "adapter"
ADAPTER_BIN_LOCAL = THIS_DIR + "/" + ADAPTER_NAME
ADAPTER_BIN = "/data/" + ADAPTER_NAME


def setup():
    logger.info("adapter setup")
    cleanup()
    check_build_env()
    get_hcfs_lib_from_phone()
    build_hcfs_adapter()
    install_hcfs_adapter_to_phone()


def check_build_env():
    if not os.environ['ANDROID_NDK']:
        raise EnvironmentError("ANDROID_NDK environment var not found.")
    adb.check_availability()


def get_hcfs_lib_from_phone():
    adb.pull_as_root(HCFS_LIB_PHONE_PATH, HCFS_LIB)
    if not os.path.isfile(HCFS_LIB):
        raise Exception("Fail to adb pull API so file.")


def build_hcfs_adapter():
    makeUtils.make(THIS_DIR)
    if not os.path.isfile(ADAPTER_BIN_LOCAL):
        raise Exception("Fail to make adapter.")


def install_hcfs_adapter_to_phone():
    adb.push_as_root(ADAPTER_BIN_LOCAL, ADAPTER_BIN)
    if not android_fileUtils.is_existed(ADAPTER_BIN):
        raise Exception("Fail to adb push adapter bin.")


def exec_api(opt):
    cmd = "su 0 ." + ADAPTER_BIN + " " + opt
    out, err = adb.exec_shell(cmd)
    logger.debug("exec_api" + repr((cmd, out, err)))
    if err:
        raise Exception(err)
    return json.loads(out)


def get_stat():
    return exec_api("stat")


def get_vol_used():
    return long(get_stat()["data"]["vol_used"])


def get_max_cache():
    return long(get_stat()["data"]["cache_total"])


def get_used_cache():
    return long(get_stat()["data"]["cache_used"])


def get_dirty():
    return long(get_stat()["data"]["cache_dirty"])


def get_cache_free_space():
    return get_max_cache() - get_used_cache()


def get_max_pin():
    return long(get_stat()["data"]["pin_max"])


def get_total_pin():
    return long(get_stat()["data"]["pin_total"])


def get_pin_free_space():
    return get_max_pin() - get_total_pin()


def pin(path):
    return exec_api("pin " + path)


def isPin(path):
    cmd = "status " + path
    return False if exec_api(cmd)["code"] == 0 else True


def unpin(path):
    return exec_api("unpin " + path)


def reload_conf():
    return exec_api("reload")


def set_sync_point():
    return exec_api("setsync")


def set_notify_server(address):
    return exec_api("setnotify " + address)


def set_log_level(level=10):
    adb.exec_shell("su 0 HCFSvol changelog " + str(level))


def is_hcfs_ok():
    stat = get_stat()
    if stat["result"] and stat["code"] == 0:
        return True
    return False


def check_if_hcfs_is_ok():
    if not is_hcfs_ok():
        raise Exception("Fail to call HCFS API code. HCFS is crash.")


def cleanup():
    logger.info("adapter cleanup")
    uninstall_hcfs_adapter_from_phone()
    make_clean()
    clean_env()


def uninstall_hcfs_adapter_from_phone():
    android_fileUtils.rm(ADAPTER_BIN)
    if android_fileUtils.is_existed(ADAPTER_BIN):
        raise Exception("Fail to rm adapter bin in phone.")


def make_clean():
    makeUtils.make(THIS_DIR, "clean")
    if os.path.isfile(ADAPTER_BIN_LOCAL):
        raise Exception("Fail to make clean adapter")


def clean_env():
    if os.path.isfile(HCFS_LIB):
        os.remove(HCFS_LIB)
        if os.path.isfile(HCFS_LIB):
            raise Exception("Fail to clean hcfs lib.")


if __name__ == '__main__':
    test_target_path = "/storage/emulated/0/DCIM/Camera"
    setup()
    # print set_sync_point()
    # set_log_level(10)
    # adb.get_logcat("tmp/logcat")
    # adb.get_hcfs_log("tmp")
    print repr(stat())
    # print "cache " + repr(get_max_cache())
    # print "max pin " + repr(get_max_pin())
    # print "dirty " + repr(get_dirty())
    # print repr(isPin(test_target_path))
    # print repr(pin(test_target_path))
    # print repr(isPin(test_target_path))
    # print repr(unpin(test_target_path))
    # print repr(isPin(test_target_path))
    # cleanup()
