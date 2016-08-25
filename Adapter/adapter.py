import os
import subprocess
from subprocess import Popen, PIPE
import json

import config
import adb

logger = config.get_logger().getChild(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

SO_PHONE_PATH = "/system/lib64/libHCFS_api.so"
SO_NAME = "libHCFS_api.so"
SO_LOCAL_PATH = THIS_DIR + "/" + SO_NAME

ADAPTER_NAME = "adapter"
ADAPTER_BIN_LOCAL = THIS_DIR + "/" + ADAPTER_NAME
ADAPTER_BIN = "/data/" + ADAPTER_NAME


def setup():
    logger.info("adapter setup")
    cleanup()
    assert os.environ['ANDROID_NDK'], "ANDROID_NDK environment var not found."
    assert adb.isAvailable(), "Adb device not found."
    if not os.path.isfile(SO_LOCAL_PATH):
        adb.get_file(SO_NAME, SO_PHONE_PATH, SO_LOCAL_PATH)
        assert os.path.isfile(SO_LOCAL_PATH), "Fail to adb pull API so file."

    cmd = "cd " + THIS_DIR + " && make"
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE,
                            stderr=PIPE, cwd=THIS_DIR)
    pipe.communicate()
    assert os.path.isfile(ADAPTER_BIN_LOCAL), "Fail to make adapter."

    adb.push_as_root(ADAPTER_BIN_LOCAL, ADAPTER_BIN, ADAPTER_NAME)
    assert adb.is_file_available(
        ADAPTER_BIN), "Fail to adb push adapter bin."
    stat()  # test by calling getHCFSstat API


def exec_api(opt, timeout=0):
    cmd = "." + ADAPTER_BIN + " " + opt
    out, err = adb.exec_cmd(cmd, timeout)
    logger.debug("exec_api" + repr((cmd, out, err)))
    assert not err, err
    return json.loads(out)


def stat():
    return exec_api("stat")


def get_vol_used():
    return long(stat()["data"]["vol_used"])


def get_max_cache():
    return long(stat()["data"]["cache_total"])


def get_used_cache():
    return long(stat()["data"]["cache_used"])


def get_dirty():
    return long(stat()["data"]["cache_dirty"])


def get_cache_stat():
    return get_max_cache(), get_used_cache()


def get_max_pin():
    return long(stat()["data"]["pin_max"])


def get_total_pin():
    return long(stat()["data"]["pin_total"])


def get_pin_stat():
    return get_max_pin(), get_total_pin()


def pin(path):
    return exec_api("pin " + path)


def isPin(path):
    cmd = "status " + path
    return False if exec_api(cmd)["code"] == 0 else True


def unpin(path):
    return exec_api("unpin " + path)


def unpin_all(path):
    unpin(path)


def reload_conf():
    return exec_api("reload")


def set_sync_point():
    return exec_api("setsync")


def set_notify_server(address):
    return exec_api("setnotify " + address)


def set_hcfs_log_level(level=10):
    adb.exec_cmd("HCFSvol changelog " + str(level))


def cleanup():
    logger.info("adapter cleanup")
    if adb.is_file_available(ADAPTER_BIN):
        adb.rm_file(ADAPTER_BIN)
        assert not adb.is_file_available(
            ADAPTER_BIN), "Fail to rm adapter bin."

    cmd = "make clean"
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE,
                            stderr=PIPE, cwd=THIS_DIR)
    pipe.communicate()
    assert not os.path.isfile(ADAPTER_BIN_LOCAL), "Fail to make clean adapter."

    cmd = "rm -f " + SO_LOCAL_PATH
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.communicate()
    assert not os.path.isfile(SO_LOCAL_PATH), "Fail to clean API so file."

if __name__ == '__main__':
    import logging
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
