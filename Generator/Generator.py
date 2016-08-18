import os
import subprocess
from subprocess import Popen, PIPE

import config
import adb

logger = config.get_logger().getChild(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

BIN_NAME = "FGen"
BIN_LOCAL_PATH = THIS_DIR + "/FGen"
BIN_PHONE_PATH = "/data/FGen"


def setup():
    logger.info("setup")
    cleanup()
    assert os.environ['ANDROID_NDK'], "ANDROID_NDK environment var not found."
    assert adb.isAvailable(), "Adb device not found."

    cmd = "make"
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE,
                            stderr=PIPE, cwd=THIS_DIR)
    out, err = pipe.communicate()
    logger.debug("setup" + repr((cmd, out, err)))
    assert os.path.isfile(BIN_LOCAL_PATH), "Fail to make adapter."

    adb.push_as_root(BIN_LOCAL_PATH, BIN_PHONE_PATH, BIN_NAME)
    assert adb.is_file_available(
        BIN_PHONE_PATH), "Fail to adb push adapter bin file."


def gen(num, size, path):
    #assert _is_setup, "Must call API after setup."
    cmd = "." + BIN_PHONE_PATH
    cmd = cmd + " " + str(num) + " " + str(size) + " " + path
    return adb.exec_cmd(cmd)


def gen_large_file(file_path, size):
    size_1m = 1048576
    assert (size % size_1m) == 0, "Size must be a factor of 1M in bytes"
    count = size / size_1m
    cmd = "dd if=/dev/zero "
    cmd = cmd + " of=" + file_path
    cmd = cmd + "  bs=" + str(size_1m) + "  count=" + str(count)
    return adb.exec_cmd(cmd)


def gen_small_file(file_path, size):
    size_1g = 1073741824
    assert size < size_1g, "Size too large, use dd instead."
    cmd = "dd if=/dev/zero of=" + file_path
    cmd = cmd + "  bs=" + str(size) + " count=1"
    return adb.exec_cmd(cmd)


def gen_1m_align_files(number, size, path):
    size_1m = 1024 * 1024
    count = size / size_1m  # 1M align
    for i in range(1, number + 1):
        file_name = str(i) + ".file"
        file_path = os.path.join(path, file_name)
        cmd = "dd if=/dev/zero of=" + file_path
        cmd += " bs=" + str(size_1m) + " count=" + str(count)
        adb.exec_cmd(cmd)


def modify_files_1m_data(begin, end, path):
    # modify 1M
    size_1m = 1024 * 1024
    for i in range(begin, end + 1):
        file_name = str(i) + ".file"
        file_path = os.path.join(path, file_name)
        cmd = "dd conv=notrun if=/dev/urandom of=" + file_path
        cmd += " bs=" + str(size_1m) + " count=1"
        adb.exec_cmd(cmd)


def fill_pictures(path, total_size):
    """
    Picture (sequencial) 800K~4M (Front camera 1080p 800K~1M, back camera 4K 2.5M~4M)
    Users rarely change resolution of phone camera.
    Fix size for this version
    """
    size = 2097152L  # 2M aveage
    num = total_size / size + 10
    gen(num, size, path)
    return num


def fill_videos(path, total_size):
    """
    # Video (sequencial) Front camera 1080p 122M/m, back camera 4K 300M/m
    Fix size for this version
    """
    size = 26214400L  # 2.5M
    num = total_size / size + 1
    gen(num, size, path)

# Document (sparse and random access) 4K~3M
# Web content (sparse and random access) 4K~200K


def cleanup():
    logger.info("cleanup")
    if adb.is_file_available(BIN_PHONE_PATH):
        adb.rm_file(BIN_PHONE_PATH)
        assert not adb.is_file_available(
            BIN_PHONE_PATH), "Fail to clean adapter bin file."

    cmd = "make clean"
    pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE,
                            stderr=PIPE, cwd=THIS_DIR)
    pipe.communicate()
    assert not os.path.isfile(BIN_LOCAL_PATH), "Fail to make clean adapter."

if __name__ == '__main__':
    import datetime
    test_dir_path = "/storage/emulated/0/testMaxPin"
    setup()
    adb.rm_file(test_dir_path)
    adb.gen_dir(test_dir_path)
    before = datetime.datetime.now()
    gen(2000, 2097152, test_dir_path)
    # gen(5000, 1048576, test_dir_path)
    after = datetime.datetime.now()
    delta = after - before

    try:
        input("Press enter to continue")
    except SyntaxError:
        pass

    adb.rm_file(test_dir_path)
    print str(delta.total_seconds()) + "seconds"
    cleanup()
