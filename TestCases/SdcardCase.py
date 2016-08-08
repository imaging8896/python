import time
from datetime import datetime

from Case import Case
import config

from Utils.timeout import timeout, TimeoutError
from Adapter import adapter
from Utils import HCFSLogUtils
from Utils import adb

# Test config, do not change these value during program.
# These vars are static final in term of Java.
PAUSED_PATTERN = "pinning manager takes a break"
#paused_pattern2 = "sync paused. pinning manager takes a break"
SYNCING_PATTERN = "datasync: start to sync"
#syncing_pattern2 = "start to put"

TEST_DIR_PATH = "/sdcard/TestCacheMgmt"
################## test config ##################


class ExpectError(Exception):
    pass


class Normal(Case):
    """
    pause-resume cache management:
          1.Gen a 10M file in /sdcard
          2.sync all data to cloud
          3. (Expected) the cache management should be paused
          4.Gen a 10M file in /sdcard
          5.(Expected) the cache management should be syncing
    """

    def setUp(self):
        self.logger = config.get_logger().getChild(self.__class__.__name__)
        self.logger.info(self.__class__.__name__)
        self.logger.info("Setup")
        self.HCFS_log = HCFSLogUtils.create_HCFS_log_obj()
        adb.enable_wifi()
        self.logger.info("Setup test dir")
        adb.rm_file(TEST_DIR_PATH)
        adb.gen_dir(TEST_DIR_PATH)

    def test(self):
        try:
            self.gen_file(TEST_DIR_PATH + "/test1.f", 10 * 1024 * 1024)
            self.sync()
            self.assert_pattern(self.HCFS_log, PAUSED_PATTERN)
            self.gen_file(TEST_DIR_PATH + "/test2.f", 10 * 1024 * 1024)
            self.assert_pattern(self.HCFS_log, SYNCING_PATTERN)
            return True, ""
        except TimeoutError:
            return False, "Sync timeout"
        except ExpectError as ee:
            return False, ee.args[0]

    def tearDown(self):
        self.logger.info("Teardown")
        self.logger.info("Teardown test dir")
        adb.rm_file(TEST_DIR_PATH)

    def gen_file(self, file, size):
        self.logger.info("Gen 10M file with full path name=" + file)
        size_1m = 1048576
        count = size / size_1m
        cmd = "dd if=/dev/zero of=" + file + " "
        cmd += "bs=" + str(size_1m) + " count=" + str(count)
        adb.exec_cmd(cmd)

    @timeout(1200, "Sync timeout.")
    def sync(self):
        self.logger.info("Wait sync finished.")
        dirty = adapter.get_dirty()
        # Define sync OK when dirty is less than 1M
        while dirty > (1024 * 1024):
            time.sleep(5)
            dirty = adapter.get_dirty()

    def assert_pattern(self, logs, pattern, timeout_sec=None):
        self.logger.info("Assert there should be a pattern in the next secs.")
        self.logger.info("Pattern='" + pattern + "'")
        if timeout_sec:
            isMatch, timestamp, log = logs.find_until(pattern, timeout_sec)
        else:
            isMatch, timestamp, log = logs.find_until(pattern)
        self.logger.debug(repr((isMatch, timestamp, log)))
        if not isMatch:
            raise ExpectError("Expect '" + pattern + "'.")
        else:
            return timestamp

    def assert_no_pattern(self, logs, pattern, timeout_sec):
        self.logger.info("Assert there is no pattern in the next secs.")
        self.logger.info("Pattern='" + pattern + "'")
        try:
            self.assert_pattern(logs, pattern, timeout_sec)
        except ExpectError:
            return True
        raise ExpectError("Expect no '" + pattern + "'.")


# inheritance Normal(setUp, tearDown, assert...)
class BackendDisconnected(Normal):
    """
    pause-resume cache management -- backend disconnected:
        1.Gen a 10M file in /sdcard
        2.sync all data to cloud
        3. (Expected) the cache management should be paused
        4.disconnect phone's connection with backend 5 minutes
        5.Gen a 10M file in /sdcard
        6.(Expected) the cache management should be paused
    """

    def test(self):
        try:
            self.gen_file(TEST_DIR_PATH + "/test1.f", 10 * 1024 * 1024)
            self.sync()
            self.assert_pattern(self.HCFS_log, PAUSED_PATTERN)
            adb.disable_wifi()
            time.sleep(10)  # wait wifi off
            self.gen_file(TEST_DIR_PATH + "/test2.f", 10 * 1024 * 1024)
            self.assert_pattern(self.HCFS_log, PAUSED_PATTERN)
            self.assert_no_pattern(self.HCFS_log, SYNCING_PATTERN, 60)
            return True, ""
        except TimeoutError:
            return False, "Sync timeout"
        except ExpectError as ee:
            return False, ee.args[0]


# inheritance Normal(setUp, tearDown, assert...)
class BackendRestored(Normal):
    """
    pause-resume cache management -- backend connection restored:
        1.Gen a 10M file in /sdcard
        2.sync all data to cloud
        3. (Expected) the cache management should be paused
        4.disconnect phone's connection with backend 5 minutes
        5.Gen a 10M file in /sdcard
        6.connect phone with backend
        7.(Expected) the cache management should be syncing
    """

    def test(self):
        try:
            self.gen_file(TEST_DIR_PATH + "/test1.f", 10 * 1024 * 1024)
            self.sync()
            self.assert_pattern(self.HCFS_log, PAUSED_PATTERN)
            adb.disable_wifi()
            time.sleep(300)  # wait wifi off 5 minute
            self.gen_file(TEST_DIR_PATH + "/test2.f", 10 * 1024 * 1024)
            adb.enable_wifi()
            self.assert_pattern(self.HCFS_log, SYNCING_PATTERN)
            return True, ""
        except TimeoutError:
            return False, "Sync timeout"
        except ExpectError as ee:
            return False, ee.args[0]
