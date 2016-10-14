import json

from socketUtils import socketToMgmtApp
import LogcatUtils

MGMT_APP_PKG = "com.hopebaytech.hcfsmgmt"
MGMT_APP_MAIN = "main.MainActivity"


def is_notify_server_can_receive_event():
    try:
        socketToMgmtApp.setup()
        LogcatUtils.clear_logcat()
        socketToMgmtApp.refresh_token()
        logcat = LogcatUtils.create_logcat_obj("TeraService")
        isFound, _, _ = logcat.find_until("eventID = 1")
        # 10-07 09:09:04.837  4737  4752 D TeraApiServer: [{"event_id":1}]
        # 10-07 09:09:04.839  4737  5414 W TeraService: TeraApiServer(run): eventID = 1
        # 10-07 09:09:04.842  4410  4410 D HopeBay :
        # HCFSMgmtReceiver(onReceive): action=hbt.intent.action.TOKEN_EXPIRED
        return isFound
    finally:
        socketToMgmtApp.cleanup()


def check_if_mgmt_app_is_ok():
    if not is_notify_server_can_receive_event():
        raise Exception(
            "Management app notify server is running but not function well.")

if __name__ == '__main__':
    print check_if_mgmt_app_is_ok()
