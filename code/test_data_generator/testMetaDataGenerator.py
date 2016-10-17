import os
import time
import shutil
import string
import random

from Utils import config
from Utils.swift import Swift
from Utils import LogcatUtils
from Utils.socket import socketToMgmtApp
from Utils import HCFSConf
from Utils import adb


class TestMetaDataGenerator(object):

    def __init__(self, phone_id, fsmgr, test_data_dir, pathes, swift):
        self.logger = config.get_logger().getChild(__name__)
        self.phone_id = phone_id
        self.fsmgr = fsmgr
        self.test_data_dir = test_data_dir
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        os.makedirs(self.test_data_dir)
        self.random_dir = os.path.join(self.test_data_dir, "random")
        os.makedirs(self.random_dir)
        self.stats = [self.get_file_stat(path) for path in pathes]
        self.swift = swift

    def get_data(self):
        if not self.is_available():
            return False
        self.get_swift_list()
        self.get_partition_stat()
        self.get_fsstat()
        self.get_random_data()
        self.get_fsmgr()
        self.get_test_data_stat()
        self.get_test_data_meta()
        return True

    def is_available(self):
        # TODO: swift server binds account, maybe we can change checking rule...
        # TODO: adb in docker, need 1.debug bridge, 2.devices
        # access to usb
        self.logger.info("Check if the USB-connected phone is Ted phone")
        return False if not adb.is_available(self.phone_id) else True

    def get_swift_list(self):
        self.logger.info("Get swift list")
        swift_list_path = os.path.join(self.test_data_dir, "swift_list")
        tmp_path = os.path.join(self.test_data_dir, "tmp")
        with open(swift_list_path, "wt") as swift_list:
            self.swift.download_file(None, tmp_path)
            marker = ""
            while True:
                with open(tmp_path, "rt") as fin:
                    files = fin.readlines()
                    if files[-1] == marker + "\n":
                        os.remove(tmp_path)
                        return
                    swift_list.write("".join(files))
                    marker = files[-1].replace("\n", "")
                self.swift.download_list_from_marker(tmp_path, marker)

    def get_partition_stat(self):
        # TODO multiple external volume???
        with open(os.path.join(self.test_data_dir, "fsmgr_stat"), "wt") as fsmgr_stat:
            self.logger.info("Get /sdcard stat")
            fsmgr_stat.write(repr(self.get_file_stat("/storage/emulated")))
        with open(os.path.join(self.test_data_dir, "data_stat"), "wt") as data_stat:
            self.logger.info("Get /data/data stat")
            data_stat.write(repr(self.get_file_stat("/data/data")))
        with open(os.path.join(self.test_data_dir, "app_stat"), "wt") as app_stat:
            self.logger.info("Get /data/app stat")
            app_stat.write(repr(self.get_file_stat("/data/app")))

    def get_fsstat(self):
        self.logger.info("Get FSstat")
        with open(os.path.join(self.test_data_dir, "swift_list"), "rt") as swift_list:
            for file in (x.replace("\n", "") for x in swift_list):
                if file.startswith("FSstat"):
                    self.logger.info("<" + file + ">")
                    fsstat_path = os.path.join(self.test_data_dir, file)
                    self.swift.download_file(file, fsstat_path)

    def get_random_data(self):
        with open(os.path.join(self.random_dir, "empty"), "wt") as empty:
            self.logger.info("Get empty content file")
        with open(os.path.join(self.random_dir, "random"), "wt") as random:
            self.logger.info("Get random content file")
            random.write(self.get_random_string(30))
        with open(os.path.join(self.test_data_dir, "swift_list"), "rt") as swift_list:
            self.logger.info("Get data block file")
            files = [x.replace("\n", "") for x in swift_list]

            def download(prefix):
                file = [x for x in files if x.startswith(prefix)][0]
                new_path = os.path.join(self.random_dir, file)
                self.swift.download_file(file, new_path)
            download("FSmgr")
            download("FSstat")
            download("data")
            download("meta")

    def get_fsmgr(self):
        self.logger.info("Get fsmgr")
        src = "/data/hcfs/metastorage/fsmgr"
        adb.get_file("fsmgr", src, self.fsmgr, self.phone_id)

    def get_test_data_meta(self):
        self.logger.info("Get metas")
        for stat in self.stats:
            inode = str(stat["stat"]["ino"])
            meta_name = "meta_" + inode
            new_path = os.path.join(self.test_data_dir, inode, meta_name)
            self.swift.download_file(meta_name, new_path)

    def get_test_data_stat(self):
        self.logger.info("Get stats")
        for stat in self.stats:
            self.logger.info("Create directory to store test data")
            inode = str(stat["stat"]["ino"])
            new_dir = os.path.join(self.test_data_dir, inode)
            os.makedirs(new_dir)
            with open(os.path.join(new_dir, inode), "wt") as stat_file:
                stat_file.write(repr(stat))

    def get_file_stat(self, path):
        result = {}
        result["file_type"] = self.stat_file_type(path)
        if result["file_type"] == 0:  # directory
            result["child_number"] = self.stat_child(path)
        else:
            result["child_number"] = 0
        result["result"] = 0
        if path.startswith("/sdcard/") or path.startswith("/storage/emulated/"):
            result["location"] = "sdcard"
        else:
            result["location"] = "local"
        stat = {}
        stat["blocks"] = self.stat_blocks(path)
        stat["ctime"] = self.stat_ctime(path)
        stat["mtime_nsec"] = 0
        stat["rdev"] = 0  # TODO: how to get this value???
        stat["dev"] = self.stat_dev(path)  # TODO: how to get this value???
        stat["mode"] = self.stat_mode(path)
        stat["__pad1"] = 0
        stat["ctime_nsec"] = 0
        stat["nlink"] = self.stat_nlink(path)
        stat["gid"] = self.stat_gid(path)
        stat["ino"] = int(self.stat_inode(path))
        stat["blksize"] = self.stat_blksize(path)
        stat["atime_nsec"] = 0
        stat["mtime"] = self.stat_mtime(path)
        stat["uid"] = self.stat_uid(path)
        stat["atime"] = self.stat_atime(path)
        stat["size"] = self.stat_size(path)  # byte
        result["stat"] = stat
        return result

    def stat_file_type(self, path):
        file_type = self.stat("F", path)
        if file_type == "directory":
            return 0
        elif file_type == "regular file":
            return 1
        elif file_type == "socket":
            return 4
        # TODO: link, pipe
        return -1

    def stat_child(self, path):
        cmd = "find " + path + " -mindepth 1 -maxdepth 1 | wc -l"
        out, err = adb.exec_cmd(cmd, self.phone_id)
        if err:
            raise Exception("Stat <" + path + "> error")
        if not out.rstrip().isdigit():
            raise Exception("Stat error child number is not a integer")
        return int(out.rstrip()) + 2  # . and ..

    def stat_inode(self, path): return self.stat("i", path)

    def stat_blocks(self, path): return int(self.stat("b", path))

    def stat_blksize(self, path): return int(self.stat("B", path))

    def stat_uid(self, path): return int(self.stat("u", path))

    def stat_gid(self, path): return int(self.stat("g", path))

    def stat_atime(self, path): return int(self.stat("X", path))

    def stat_mtime(self, path): return int(self.stat("Y", path))

    def stat_ctime(self, path): return int(self.stat("Z", path))

    def stat_nlink(self, path): return int(self.stat("h", path))

    def stat_dev(self, path): return int(self.stat("d", path)[:-1])

    def stat_mode(self, path): return int(self.stat("f", path), 16)

    def stat_size(self, path): return int(self.stat("s", path))

    def stat(self, opt, path):
        cmd = "stat -c%" + opt + " " + path
        out, err = adb.exec_cmd(cmd, self.phone_id)
        if err:
            raise Exception("Stat <" + path + "> error")
        if not out:
            raise Exception("Stat <" + path + "> result is empty")
        return out.rstrip()

    def get_random_string(self, size=6, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    socketToMgmtApp.setup()
    socketToMgmtApp.refresh_token()
    socketToMgmtApp.cleanup()
    time.sleep(5)

    HCFSConf.setup()

    logcat = LogcatUtils.create_logcat_obj("HopeBay")
    isFound, timestamp, log = logcat.find_until("setSwiftToken")
    if not isFound:
        raise Exception(
            "Timeout while finding setSwiftToken API log in logcat")
    # HCFSMgmtUtils(setSwiftToken): what we need
    content = log.split(":", 1)[1].strip()
    # url=https://61.219.202.83:8080/swift/v1, token=XXXX,
    # result={"result":true,"code":0,"data":{}}
    url = content.split(", ")[0].split("=")[1]
    token = content.split(", ")[1].split("=")[1]
    json_result = content.split(", ")[2].split("=")[1]

    swift = Swift.via_token(url, HCFSConf.get_container(), token)
    HCFSConf.cleanup()

    this_dir = os.path.abspath(os.path.dirname(__file__))
    test_data_dir = os.path.join(this_dir, "..", "TestCases", "test_data_v2")
    phone_id = "00f28ec4cb50a4f2"
    fsmgr = os.path.join(test_data_dir, "fsmgr")
    inodes = ["/sdcard/DCIM/", "/sdcard/1.f", "/data/data/2.f",
              "/data/data/com.hopebaytech.hcfsmgmt/hcfsapid_sock", "/data/data/com.hopebaytech.hcfsmgmt/databases/"]
    param = (phone_id, fsmgr, test_data_dir, inodes, swift)

    testDataGener = TestMetaDataGenerator(*param)
    testDataGener.get_data()
