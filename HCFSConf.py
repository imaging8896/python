import os
import subprocess
from subprocess import Popen, PIPE
import tempfile

import adb
import config

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
HCFSCONF_BIN_DIR = os.path.join(THIS_DIR, "hcfsconf")
HCFSCONF_BIN = os.path.join(HCFSCONF_BIN_DIR, "hcfsconf")

HCFSCONF_ENC_FILE = "hcfs.conf"
HCFSCONF_ENC_FILE_PATH = os.path.join("/data", HCFSCONF_ENC_FILE)
HCFSCONF_FILE = "hcfs.conf.plain"

serialno = ""
logger = config.get_logger().getChild(__name__)


def setup():
    logger.info("hcfsconf setup")
    cleanup()
    assert adb.isAvailable(), "Adb device not found."

    cmd = "cd " + HCFSCONF_BIN_DIR + " && make hcfsconf"
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.communicate()
    assert os.path.isfile(HCFSCONF_BIN), "Fail to make hcfsconf."

    adb.get_file(HCFSCONF_ENC_FILE, HCFSCONF_ENC_FILE_PATH, THIS_DIR, serialno)

    enc_path = os.path.join(THIS_DIR, HCFSCONF_ENC_FILE)
    plain_path = os.path.join(THIS_DIR, HCFSCONF_FILE)
    cmd = "cd " + HCFSCONF_BIN_DIR + " && ./hcfsconf dec " + enc_path + " " + plain_path
    pipe = subprocess.Popen(cmd, shell=True)
    out, err = pipe.communicate()
    logger.debug(repr((out, err)))
    assert os.path.isfile(plain_path), "Fail to dec hcfs.conf."


def get_container():
    value = get_by_key("SWIFT_CONTAINER")
    assert value, "Fail to parse 'container' from dec hcfs.conf file"
    return value


def get_by_key(key):
    # TODO class instead of dynamic parse
    plain_path = os.path.join(THIS_DIR, HCFSCONF_FILE)
    with open(plain_path, "rt") as fin:
        for line in fin:
            cur_key = line.split(" = ", 2)[0]
            if cur_key == key:
                return line.split(" = ", 2)[1].replace("\n", "")
    return ""


def cleanup():
    logger.info("hcfsconf cleanup")
    cmd = "cd " + HCFSCONF_BIN_DIR + " && make clean"
    pipe = subprocess.Popen(cmd, shell=True)
    pipe.communicate()
    assert not os.path.isfile(HCFSCONF_BIN), "Fail to make clean hcfsconf."

    try:
        os.remove(os.path.join(THIS_DIR, HCFSCONF_ENC_FILE))
        os.remove(os.path.join(THIS_DIR, HCFSCONF_FILE))
    except OSError:
        pass


if __name__ == "__main__":
    setup()
    # cleanup()
