import os
from subprocess import Popen, PIPE

import config
import makeUtils
from ..adb.factory import *

logger = config.get_logger().getChild(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

BIN_NAME = "socketToMgmtApp"
BIN_LOCAL_PATH = THIS_DIR + "/socketToMgmtApp"
BIN_PHONE_PATH = "/data/socketToMgmtApp"

EVENT_CONNECTED = 0
EVENT_TOKEN_EXPIRED = 1


def setup():
    logger.info("socket setup")
    check_build_env()
    cleanup()
    build_socket_utils()
    install_socket_utils_to_phone()


def check_build_env():
    if not os.environ['ANDROID_NDK']:
        raise EnvironmentError("ANDROID_NDK environment var not found.")
    adb.check_availability()


def build_socket_utils():
    makeUtils.make(THIS_DIR)
    if not os.path.isfile(BIN_LOCAL_PATH):
        raise Exception("Fail to make.")


def install_socket_utils_to_phone():
    adb.push_as_root(BIN_LOCAL_PATH, BIN_PHONE_PATH)
    if not android_fileUtils.is_existed(BIN_PHONE_PATH):
        raise Exception("Fail to adb push bin file.")


def send_connected_event():
    return send_event(EVENT_CONNECTED)


def refresh_token():
    return send_event(EVENT_TOKEN_EXPIRED)


def send_event(event):
    cmd = ".{0} {1}".format(BIN_PHONE_PATH, event)
    return adb.exec_shell(cmd)


def cleanup():
    logger.info("socket cleanup")
    uninstall_socket_utils_from_phone()
    make_clean()


def uninstall_socket_utils_from_phone():
    android_fileUtils.rm(BIN_PHONE_PATH)
    if android_fileUtils.is_existed(BIN_PHONE_PATH):
        raise Exception("Fail to rm socket utils bin in phone.")


def make_clean():
    makeUtils.make(THIS_DIR, "clean")
    if os.path.isfile(BIN_LOCAL_PATH):
        raise Exception("Fail to make clean")


if __name__ == '__main__':
    setup()
    refresh_token()
    cleanup()
