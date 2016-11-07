from os.path import isfile as fileExists
from os.path import join as pathJoin
from os.path import dirname
from os.path import abspath

import makeUtils
import config
from ..adb.factory import *
from ..dockerBuildUtils import dockerBuildUtils

logger = config.get_logger().getChild(__name__)

THIS_DIR = abspath(dirname(__file__))

UTILS_NAME = "alias"
UTILS_LOCAL = pathJoin(THIS_DIR, UTILS_NAME)
UTILS = "/data/" + UTILS_NAME


def setup():
    logger.info("setup")
    cleanup()
    check_build_env()
    build_alias_utils()
    install_alias_utils()


def check_build_env():
    logger.info("check_build_env")
    adb.check_availability()


def build_alias_utils():
    logger.info("build_alias_util")
    dockerBuildUtils.make_ndk_build(THIS_DIR)
    if not fileExists(UTILS_LOCAL):
        raise Exception("Fail to make alias utils binary.")


def install_alias_utils():
    logger.info("install_alias_utils")
    adb.push_as_root(UTILS_LOCAL, UTILS)
    if not android_fileUtils.is_existed(UTILS):
        raise Exception("Fail to adb push alias utils binary.")


def is_alias_and_file_not_exist(file, max_alias=-1):
    """
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music")
    False
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music", 1)
    False
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music", 32)
    False
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music", 300)
    False
    >>> is_alias_and_file_not_exist("")
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> is_alias_and_file_not_exist("", 3)
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music1")
    True
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music1", 1)
    True
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music1", 32)
    True
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music1", 300)
    True
    """
    if not file:
        raise ValueError("Empty path is not allowed.")
    cmd = "su 0 .{0} {1} {2} {3}".format(UTILS, "notexist", file, max_alias)
    out, err = adb.exec_shell(cmd)
    if err:
        raise Exception(err)
    return True if not out else False


def gen_all_alias(file, max_alias=-1):
    """
    >>> gen_all_alias("/storage/emulated/0/Music")
    >>> gen_all_alias("/storage/emulated/0/Music", 1)
    >>> gen_all_alias("/storage/emulated/0/Music", 32)
    >>> gen_all_alias("/storage/emulated/0/Music", 300)
    >>> gen_all_alias("")
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> gen_all_alias("", 3)
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> gen_all_alias("/storage/emulated/0/Music1")
    Traceback (most recent call last):
        ...
    Exception: /storage/emulated/0/music1:No such file or directory
    """
    if not file:
        raise ValueError("Empty path is not allowed.")
    cmd = "su 0 .{0} {1} {2} {3}".format(UTILS, "genaliases", file, max_alias)
    out, err = adb.exec_shell(cmd)
    if err:
        raise Exception(err)
    if out:
        raise Exception(out)


def get_alias_inos(file, max_alias=-1):
    """
    >>> from code.adb.factory import *
    >>> _,_ = android_fileUtils.touch("/storage/emulated/0/abc.file")
    >>> get_alias_inos("/storage/emulated/0/abc.file")
    128
    >>> len(get_alias_inos("/storage/emulated/0/Music"))
    32
    >>> len(get_alias_inos("/storage/emulated/0/Music", 1))
    1
    >>> len(get_alias_inos("/storage/emulated/0/Music", 32))
    32
    >>> len(get_alias_inos("/storage/emulated/0/Music", 300))
    32
    >>> len(get_alias_inos("/storage/emulated/0/DCIM"))
    16
    >>> get_alias_inos("")
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> get_alias_inos("", 3)
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> get_alias_inos("/storage/emulated/0/Music1")
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: '/storage/emulated/0/music1:No such file or directory'
    >>> _,_ = android_fileUtils.rm("/storage/emulated/0/abc.file")
    """
    if not file:
        raise ValueError("Empty path is not allowed.")
    cmd = "su 0 .{0} {1} {2} {3}".format(UTILS, "getinos", file, max_alias)
    out, err = adb.exec_shell(cmd)
    if err:
        raise Exception(err)
    if not out:
        raise Exception("No output error")
    return map(int, out.strip().split("\n"))


def cleanup():
    logger.info("cleanup")
    uninstall_alias_utils()
    make_clean()


def uninstall_alias_utils():
    logger.info("uninstall_alias_utils")
    android_fileUtils.rm(UTILS)
    if android_fileUtils.is_existed(UTILS):
        raise Exception("Fail to rm alias utils binary in phone.")


def make_clean():
    logger.info("make_clean")
    makeUtils.make(THIS_DIR, "clean")
    if fileExists(UTILS_LOCAL):
        raise Exception("Fail to make clean alias utils binary")
