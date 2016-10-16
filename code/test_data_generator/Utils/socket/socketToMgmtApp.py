import os
from subprocess import Popen, PIPE

from .. import config
from .. import adb

logger = config.get_logger().getChild(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

BIN_NAME = "socketToMgmtApp"
BIN_LOCAL_PATH = THIS_DIR + "/socketToMgmtApp"
BIN_PHONE_PATH = "/data/socketToMgmtApp"

EVENT_CONNECTED = 0
EVENT_TOKEN_EXPIRED = 1


def setup():
    logger.info("socket setup")
    if not os.environ['ANDROID_NDK']:
        raise EnvironmentError("ANDROID_NDK environment var not found.")
    adb.check_availability()
    cleanup()

    cmd = "make"
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=THIS_DIR)
    out, err = process.communicate()
    logger.debug("setup" + repr((out, err)))
    if not os.path.isfile(BIN_LOCAL_PATH):
        raise Exception("Fail to make " + BIN_NAME)

    adb.push_as_root(BIN_LOCAL_PATH, BIN_PHONE_PATH, BIN_NAME)
    if not adb.is_file_available(BIN_PHONE_PATH):
        raise Exception("Fail to adb push bin file.")


def send_connected_event():
    return send_event(EVENT_CONNECTED)


def refresh_token():
    return send_event(EVENT_TOKEN_EXPIRED)


def send_event(event):
    cmd = ".{0} {1}".format(BIN_PHONE_PATH, event)
    return adb.exec_cmd(cmd)


def cleanup():
    logger.info("socket cleanup")
    if adb.is_file_available(BIN_PHONE_PATH):
        adb.rm_file(BIN_PHONE_PATH)
        if adb.is_file_available(BIN_PHONE_PATH):
            raise Exception("Fail to adb clean bin file.")

    cmd = "make clean"
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=THIS_DIR)
    process.communicate()
    if os.path.isfile(BIN_LOCAL_PATH):
        raise Exception("Fail to make clean " + BIN_NAME)

if __name__ == '__main__':
    setup()
    refresh_token()
    cleanup()
