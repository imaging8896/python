import os
from os.path import isfile as fileExists
from os.path import join as pathJoin
from os.path import dirname
from os.path import abspath
import subprocess
from subprocess import Popen, PIPE

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


def gen_all_alias(file):
    get_alias_inos(file)


def get_alias_inos(file):
    """
    >>> len(get_alias_inos("/storage/emulated/0/Music"))
    32
    >>> len(get_alias_inos("/storage/emulated/0/DCIM"))
    16
    >>> get_alias_inos("")
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Empty path is not allowed.
    >>> get_alias_inos("/storage/emulated/0/Music1")
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: invalid literal for int() with base 10: '/storage/emulated/0/Music1:No such file or directory'
    """
    if not file:
        raise ValueError("Empty path is not allowed.")
    cmd = "su 0 ." + UTILS + " " + file
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
