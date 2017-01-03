import config
import _socketToMgmtApp as socketMgmtApp
from ..adb import adb
from ..androidUtils import am
from .. import LogcatUtils
from ..hcfsUtils import hcfsUtils

logger = config.get_logger().getChild(__name__)

MGMT_APP_PKG = "com.hopebaytech.hcfsmgmt"
MGMT_APP_MAIN = "main.MainActivity"

EVENT_SERVER_TAG = "TeraService"
EVENT_SERVER_START = "Server socket run . . . start"
EVENT_SERVER_SYNC_FINISH = "eventID = 2"
EVENT_SERVER_TOKEN_EXPIRED = "eventID = 1"
EVENT_SERVER_CONNECTED = "eventID = 0"
# 10-07 09:09:04.837  4737  4752 D TeraApiServer: [{"event_id":1}]
# 10-07 09:09:04.839  4737  5414 W TeraService: TeraApiServer(run): eventID = 1
# 10-07 09:09:04.842  4410  4410 D HopeBay :
# HCFSMgmtReceiver(onReceive): action=hbt.intent.action.TOKEN_EXPIRED


def setup():
    logger.info("management app utils setup")
    socketMgmtApp.setup()


def start_app():
    am.start_activity(MGMT_APP_PKG, MGMT_APP_MAIN)


def wait_event_server_up(timeout_sec=60):
    logcat = LogcatUtils.create_logcat_obj(EVENT_SERVER_TAG)
    isFound, _, _ = logcat.find_until(EVENT_SERVER_START, timeout_sec)
    return isFound


def wait_token_expired_event(timeout_sec=60):
    logcat = LogcatUtils.create_logcat_obj(EVENT_SERVER_TAG)
    isFound, _, _ = logcat.find_until(EVENT_SERVER_TOKEN_EXPIRED, timeout_sec)
    return isFound


def wait_sync_finish(timeout_sec=180):
    logcat = LogcatUtils.create_logcat_obj(EVENT_SERVER_TAG)
    isFound, _, _ = logcat.find_until(EVENT_SERVER_SYNC_FINISH, timeout_sec)
    return isFound


def refresh_token():
    LogcatUtils.clear_logcat()
    socketMgmtApp.refresh_token()
    if not wait_token_expired_event():
        raise Exception(
            "Fail to refresh token, because timeout to wait event server receiving event.")


def is_notify_server_work():
    """
    >>> is_notify_server_work()
    True
    """
    LogcatUtils.clear_logcat()
    socketMgmtApp.refresh_token()
    return wait_token_expired_event()


def check_if_app_ok():
    if not is_notify_server_work():
        raise Exception(
            "Management app notify server can not receive event.")


def boot_and_wait_ok():
    adb.reboot()
    if not wait_event_server_up():
        raise Exception("Timeout to wait event server startup.")
    if not wait_token_expired_event():
        raise Exception("Timeout to wait token expired event.")
    hcfsUtils.check_if_hcfs_is_ok()
    hcfsUtils.wait_cloud_connected()


def cleanup():
    logger.info("management app utils cleanup")
    socketMgmtApp.cleanup()
