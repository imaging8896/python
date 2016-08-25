import os
import subprocess
from subprocess import Popen, PIPE

import config
import adb

logger = config.get_logger().getChild(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

BIN_NAME = "socketToMgmtApp"
BIN_LOCAL_PATH = THIS_DIR + "/socketToMgmtApp"
BIN_PHONE_PATH = "/data/socketToMgmtApp"


def setup():
    logger.info("socket setup")
    cleanup()
    assert os.environ['ANDROID_NDK'], "ANDROID_NDK environment var not found."
    assert adb.isAvailable(), "Adb device not found."

    cmd = "make"
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE,
                            stderr=PIPE, cwd=THIS_DIR)
    out, err = pipe.communicate()
    logger.debug("setup" + repr((out, err)))
    assert os.path.isfile(BIN_LOCAL_PATH), "Fail to make " + BIN_NAME

    adb.push_as_root(BIN_LOCAL_PATH, BIN_PHONE_PATH, BIN_NAME)
    assert adb.is_file_available(BIN_PHONE_PATH), "Fail to adb push bin file."


def refresh_token():
    #assert _is_setup, "Must call API after setup."
    cmd = "." + BIN_PHONE_PATH
    return adb.exec_cmd(cmd)


def cleanup():
    logger.info("socket cleanup")
    if adb.is_file_available(BIN_PHONE_PATH):
        adb.rm_file(BIN_PHONE_PATH)
        assert not adb.is_file_available(
            BIN_PHONE_PATH), "Fail to clean bin file."

    cmd = "make clean"
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE,
                            stderr=PIPE, cwd=THIS_DIR)
    pipe.communicate()
    assert not os.path.isfile(BIN_LOCAL_PATH), "Fail to make clean."

if __name__ == '__main__':
    setup()
    refresh_token()
    cleanup()
