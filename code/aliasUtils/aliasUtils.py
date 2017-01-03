from os.path import isfile as fileExists
from os.path import join as pathJoin
from os.path import dirname
from os.path import abspath

import makeUtils
import config
from ..adb import adb
from ..androidUtils import fileUtils
from ..dockerBuildUtils import dockerBuildUtils

logger = config.get_logger().getChild(__name__)

THIS_DIR = abspath(dirname(__file__))

UTILS_NAME = "alias"
UTILS_DIR = pathJoin(THIS_DIR, "c")
UTILS_LOCAL = pathJoin(UTILS_DIR, UTILS_NAME)
UTILS = "/data/" + UTILS_NAME


def setup():
    logger.info("setup")
    cleanup()
    build_alias_utils()
    install_alias_utils()


def build_alias_utils():
    logger.info("build_alias_util")
    dockerBuildUtils.make_ndk_build(UTILS_DIR)
    if not fileExists(UTILS_LOCAL):
        raise Exception("Fail to make alias utils binary.")


def install_alias_utils():
    logger.info("install_alias_utils")
    adb.push_as_root(UTILS_LOCAL, UTILS)
    if not fileUtils.is_existed(UTILS):
        raise Exception("Fail to adb push alias utils binary.")


def is_alias_and_file_not_exist(file):
    """
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music")
    False
    >>> is_alias_and_file_not_exist("")
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> is_alias_and_file_not_exist("/storage/emulated/0/Music1")
    True
    """
    if not file:
        raise ValueError("Empty path is not allowed.")
    cmd = "su 0 .{0} {1} {2}".format(UTILS, "allnotexist", file)
    out, err = adb.exec_shell(cmd)
    if err:
        raise Exception(err)
    return True if not out else False


def gen_all_alias(file, max_alias=0):
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
    Exception: error:fail to generate alias
    """
    if not file:
        raise ValueError("Empty path is not allowed.")
    cmd = "su 0 .{0} {1} {2} {3}".format(UTILS, "genaliases", file, max_alias)
    out, err = adb.exec_shell(cmd)
    if err:
        raise Exception(err)
    if out:
        raise Exception(out)


def get_alias_inos(file, max_alias=0):
    """
    >>> from code.androidUtils import fileUtils
    >>> _,_ = fileUtils.touch("/storage/emulated/0/abc.file")
    >>> len(get_alias_inos("/storage/emulated/0/abc.file"))
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
    ValueError: invalid literal for int() with base 10: 'error:No such file or directory'
    >>> _,_ = fileUtils.rm("/storage/emulated/0/abc.file")
    """
    if not file:
        raise ValueError("Empty path is not allowed.")
    cmd = "su 0 .{0} {1} {2} {3}".format(UTILS, "getinos", file, max_alias)
    out, err = adb.exec_shell(cmd)
    if not out:
        raise Exception("No output error")
    return map(int, out.strip().split("\n"))


def concurrent(cmds):
    # [("genalias"/"casechange"/"createremove", path) ...]
    """
    >>> from code.androidUtils import fileUtils
    >>> _,_ = fileUtils.touch("/storage/emulated/0/abc.file")
    >>> _,_ = fileUtils.touch("/storage/emulated/0/def.file")
    >>> concurrent([("genalias", "/storage/emulated/0/abc.file"), ("genalias", "/storage/emulated/0/abc.file")])
    >>> concurrent([("genalias", "/storage/emulated/0/abc.file"), ("casechange", "/storage/emulated/0/def.file"), ("createremove", "/storage/emulated/0/a.file")])
    >>> concurrent([])
    Traceback (most recent call last):
        ...
    ValueError: Empty cmds is not allowed.
    >>> concurrent([("genalias", "/storage/emulated/0/abc.file")])
    Traceback (most recent call last):
        ...
    ValueError: One cmds is not allowed(doesn't make sense).
    >>> concurrent([("asd", "asd"), ("asd", "asd")])
    Traceback (most recent call last):
        ...
    ValueError: Invalid concurrent command.
    >>> concurrent([("genalias", ""), ("asd", "asd")])
    Traceback (most recent call last):
        ...
    ValueError: Empty path is not allowed.
    >>> _,_ = fileUtils.rm("/storage/emulated/0/abc.file")
    >>> _,_ = fileUtils.rm("/storage/emulated/0/def.file")
    """
    if not cmds:
        raise ValueError("Empty cmds is not allowed.")
    if len(cmds) == 1:
        raise ValueError("One cmds is not allowed(doesn't make sense).")
    cmd = "su 0 .{0} {1}".format(UTILS, "concurrent")
    for subcmd, path in cmds:
        if subcmd not in ["genalias", "casechange", "createremove"]:
            raise ValueError("Invalid concurrent command.")
        if not path:
            raise ValueError("Empty path is not allowed.")
        cmd += " {0} {1}".format(subcmd, path)
    out, err = adb.exec_shell(cmd)
    if err:
        raise Exception(err)
    if out:
        raise Exception(out)


def cleanup():
    logger.info("cleanup")
    uninstall_alias_utils()
    make_clean()


def uninstall_alias_utils():
    logger.info("uninstall_alias_utils")
    fileUtils.rm(UTILS)
    if fileUtils.is_existed(UTILS):
        raise Exception("Fail to rm alias utils binary in phone.")


def make_clean():
    logger.info("make_clean")
    makeUtils.make(UTILS_DIR, "clean")
    if fileExists(UTILS_LOCAL):
        raise Exception("Fail to make clean alias utils binary")
