import os
import subprocess
from subprocess import PIPE
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
    adb.check_availability()

    cmd = "cd " + HCFSCONF_BIN_DIR + " && make hcfsconf"
    subprocess.call(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if not os.path.isfile(HCFSCONF_BIN):
        raise Exception("Fail to make hcfsconf.")

    adb.get_file(HCFSCONF_ENC_FILE, HCFSCONF_ENC_FILE_PATH, THIS_DIR, serialno)

    enc_path = os.path.join(THIS_DIR, HCFSCONF_ENC_FILE)
    plain_path = os.path.join(THIS_DIR, HCFSCONF_FILE)
    cmd = "cd " + HCFSCONF_BIN_DIR + " && ./hcfsconf dec " + enc_path + " " + plain_path
    subprocess.call(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if not os.path.isfile(plain_path):
        raise Exception("Fail to dec hcfs.conf.")


def get_container():
    return get_by_key("SWIFT_CONTAINER")


def get_by_key(key):
    # TODO class instead of dynamic parse
    plain_path = os.path.join(THIS_DIR, HCFSCONF_FILE)
    with open(plain_path, "rt") as fin:
        for line in fin:
            cur_key = line.split(" = ", 2)[0]
            if cur_key == key:
                return line.split(" = ", 2)[1].replace("\n", "")
    raise Exception("Fail to find key(" + key + ") from hcfs.conf file")


def cleanup():
    logger.info("hcfsconf cleanup")
    cmd = "cd " + HCFSCONF_BIN_DIR + " && make clean"
    subprocess.call(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if os.path.isfile(HCFSCONF_BIN):
        raise Exception("Fail to make clean hcfsconf.")

    try:
        os.remove(os.path.join(THIS_DIR, HCFSCONF_ENC_FILE))
        os.remove(os.path.join(THIS_DIR, HCFSCONF_FILE))
    except OSError:
        pass


if __name__ == "__main__":
    setup()
    # cleanup()
