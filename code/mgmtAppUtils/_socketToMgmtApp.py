from os.path import isfile as fileExists
from os.path import dirname
from os.path import abspath

import config
import makeUtils
from ..adb import adb
from ..androidUtils import fileUtils
from ..dockerBuildUtils import dockerBuildUtils

logger = config.get_logger().getChild(__name__)

THIS_DIR = abspath(dirname(__file__))

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
    logger.info("check_build_env")
    adb.check_availability()


def build_socket_utils():
    logger.info("build_socket_utils")
    dockerBuildUtils.make_ndk_build(THIS_DIR)
    if not fileExists(BIN_LOCAL_PATH):
        raise Exception("Fail to make.")


def install_socket_utils_to_phone():
    logger.info("install_socket_utils_to_phone")
    adb.push_as_root(BIN_LOCAL_PATH, BIN_PHONE_PATH)
    if not fileUtils.is_existed(BIN_PHONE_PATH):
        raise Exception("Fail to adb push bin file.")


def send_connected_event():
    send_event(EVENT_CONNECTED)


def refresh_token():
    send_event(EVENT_TOKEN_EXPIRED)


def send_event(event):
    cmd = "su 0 .{0} {1}".format(BIN_PHONE_PATH, event)
    for i in range(1, 5):  # retry 5 times
        out, _ = adb.exec_shell(cmd)
        if not out:
            return
    raise Exception(out)


def cleanup():
    logger.info("socket cleanup")
    uninstall_socket_utils_from_phone()
    make_clean()


def uninstall_socket_utils_from_phone():
    logger.info("uninstall_socket_utils_from_phone")
    fileUtils.rm(BIN_PHONE_PATH)
    if fileUtils.is_existed(BIN_PHONE_PATH):
        raise Exception("Fail to rm socket utils bin in phone.")


def make_clean():
    logger.info("make_clean")
    makeUtils.make(THIS_DIR, "clean")
    if fileExists(BIN_LOCAL_PATH):
        raise Exception("Fail to make clean")
