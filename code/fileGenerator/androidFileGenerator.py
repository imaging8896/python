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

# use /dev/zero is much faster than /dev/urandom

logger = config.get_logger().getChild(__name__)

THIS_DIR = abspath(dirname(__file__))

FG_BIN = pathJoin(THIS_DIR, "FileGen")
FG_PHONE_BIN = "/data/FileGen"


SINGLE_FG_BIN = pathJoin(THIS_DIR, "SingleFileGen")
S_FG_PHONE_BIN = "/data/SingleFileGen"

RANDOM_FILE_NAME = "random"
RANDOM_FILE_PHONE = "/data/random"
RANDOM_FILE = pathJoin(THIS_DIR, "random")


def setup():
    logger.info("setup")
    cleanup()
    check_build_env()
    build_file_generator()
    install_file_generator()
    prepare_file_pattern()


def check_build_env():
    logger.info("check_build_env")
    adb.check_availability()


def build_file_generator():
    logger.info("build_file_generator")
    dockerBuildUtils.make_ndk_build(THIS_DIR)
    if not fileExists(FG_BIN):
        raise Exception("Fail to make FileGen")
    if not fileExists(SINGLE_FG_BIN):
        raise Exception("Fail to make SingleFileGen")


def install_file_generator():
    logger.info("install_file_generator")
    adb.push_as_root(FG_BIN, FG_PHONE_BIN)
    if not android_fileUtils.is_existed(FG_PHONE_BIN):
        raise Exception("Fail to adb push FileGen bin file.")
    adb.push_as_root(SINGLE_FG_BIN, S_FG_PHONE_BIN)
    if not android_fileUtils.is_existed(S_FG_PHONE_BIN):
        raise Exception("Fail to adb push SingleFileGen bin file.")


def prepare_file_pattern():
    logger.info("prepare_file_pattern")
    if not fileExists(RANDOM_FILE):
        with open(RANDOM_FILE, 'w') as rand_file:
            for i in range(1, 1):
                f.write(os.urandom(1048576))
    adb.push_as_root(RANDOM_FILE, RANDOM_FILE_PHONE)
    if not android_fileUtils.is_existed(RANDOM_FILE_PHONE):
        raise Exception("Fail to adb push random file.")


def single_file_gen(path, size):
    cmd = "su 0 .{0} {1} {2}".format(S_FG_PHONE_BIN, path, str(size))
    return adb.exec_shell(cmd)


def files_gen(num, size, path):
    cmd = "su 0 .{0} {1} {2} {3}".format(
        FG_PHONE_BIN, str(num), str(size), path)
    return adb.exec_shell(cmd)


def gen_large_file(file_path, size, in_stream="/dev/zero"):
    size_1m = 1048576
    count = size / size_1m + 1
    return android_fileUtils.dd_bs_1m(file_path, count, in_stream)


def gen_small_file(file_path, size, in_stream="/dev/zero"):
    size_1g = 1073741824
    assert size < size_1g, "Size too large, use gen_large_file instead."
    return android_fileUtils.dd_one_count(file_path, size)


def gen_1m_align_files(number, size, path, in_stream="/dev/zero"):
    count = size / size_1m  # 1M align
    for i in range(1, number + 1):
        file_name = str(i) + ".file"
        file_path = os.path.join(path, file_name)
        android_fileUtils.dd_bs_1m(file_path, count, in_stream)


def modify_files_1m_data(begin, end, path):
    # modify 1M
    size_1m = 1024 * 1024
    for i in range(begin, end + 1):
        file_name = str(i) + ".file"
        file_path = os.path.join(path, file_name)
        android_fileUtils.dd_one_count(
            file_path, size_1m, "/dev/urandom", "conv=notrun")


def fill_2M(path, total_size):
    """
    Picture (sequencial) 800K~4M (Front camera 1080p 800K~1M, back camera 4K 2.5M~4M)
    Users rarely change resolution of phone camera.
    Fix size for this version
    """
    size = 2097152L  # 2M aveage
    num = total_size / size + 1
    files_gen(num, size, path)
    return num


def fill_videos(path, total_size):
    """
    # Video (sequencial) Front camera 1080p 122M/m, back camera 4K 300M/m
    Fix size for this version
    """
    size = 26214400L  # 2.5M
    num = total_size / size + 1
    files_gen(num, size, path)

# Document (sparse and random access) 4K~3M
# Web content (sparse and random access) 4K~200K


def cleanup():
    logger.info("cleanup")
    uninstall_file_generator_from_phone()
    make_clean()


def uninstall_file_generator_from_phone():
    logger.info("uninstall_file_generator_from_phone")
    android_fileUtils.rm(FG_PHONE_BIN)
    if android_fileUtils.is_existed(FG_PHONE_BIN):
        raise Exception("Fail to clean FileGen bin file.")
    android_fileUtils.rm(S_FG_PHONE_BIN)
    if android_fileUtils.is_existed(S_FG_PHONE_BIN):
        raise Exception("Fail to clean SingleFileGen bin file.")


def make_clean():
    logger.info("make_clean")
    makeUtils.make(THIS_DIR, "clean")
    if fileExists(FG_BIN):
        raise Exception("Fail to make clean FileGen")
    if fileExists(SINGLE_FG_BIN):
        raise Exception("Fail to make clean SingleFileGen")

if __name__ == '__main__':
    import datetime
    test_dir_path = "/storage/emulated/0/testMaxPin"
    setup()
    android_fileUtils.rm(test_dir_path)
    android_fileUtils.mkdir(test_dir_path)
    before = datetime.datetime.now()
    gen(2000, 2097152, test_dir_path)
    # gen(5000, 1048576, test_dir_path)
    after = datetime.datetime.now()
    delta = after - before

    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

    android_fileUtils.rm(test_dir_path)
    print str(delta.total_seconds()) + "seconds"
    cleanup()
