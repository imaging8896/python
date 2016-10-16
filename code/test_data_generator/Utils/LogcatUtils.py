from datetime import datetime
from subprocess import Popen, PIPE
import time


class Logcat(object):
    """
    Logcat format:
    08-15 08:36:43.657  4394  5658 W HopeBay : TeraAPIServer->MgmtApiUtils(run): eventID=1
    08-15 08:36:43.729  4394  4394 D HopeBay : GoogleSignInApiClient(onConnected):

    We parse to [(datetime, level, log), ...] and store it to Logcat object.
    ex:  [(datetime, "W", "loglog"), ...] 
    time format : "%m-%d %H:%M:%S.%f"
    """

    def __init__(self, input_tag):
        self.TIME_FMT = "%m-%d %H:%M:%S.%f"
        self.tag = input_tag
        self.logs = self.parse(self.get_raw_logcat())

    def refresh(self):
        new_logs = self.parse(self.get_raw_logcat())
        if not self.logs:
            self.logs = new_logs
            return
        last_time, _, last_log = self.logs[-1]
        for i, (timestamp, _, log) in enumerate(new_logs):
            if timestamp == last_time and log == last_log:
                self.logs = new_logs[i:]
                return
        self.logs = new_logs

    def find_until(self, pattern, timeout_sec=300, interval=10):
        for _ in range(1, timeout_sec / interval):
            for timestamp, _, log in self.logs:
                if pattern in log:
                    return True, timestamp, log
            time.sleep(interval)
            self.refresh()
        return False, None, None

    def parse(self, logs_str):
        # parse to [(datetime object, log string), ...]
        # Seperate by line
        lines = logs_str.split("\r\n")
        # Seperate by ":". Keep log which matches "time, tag and type:log"
        lines = [tuple(line.split(" : ")) for line in lines if line]
        result = []
        for forepart, log in [pair for pair in lines if len(pair) == 2]:
            # 08-15 08:36:43.657  4394  5658 W HopeBay
            pieces = filter(None, forepart.split(" "))
            if len(pieces) != 6:
                continue
            timestamp = pieces[0] + " " + pieces[1]
            level = pieces[4]
            if not self.validate_date(timestamp):
                continue
            one_log = (datetime.strptime(timestamp, self.TIME_FMT), level, log)
            result += [one_log]
        return result

    def get_raw_logcat(self):
        cmd = "adb logcat -d"
        if self.tag:
            cmd += " -s " + self.tag
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        if err:
            raise Exception(err)
        return out

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, self.TIME_FMT)
            return True
        except ValueError as a:
            return False


def clear_logcat():
    cmd = "adb logcat -c "
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    return out, err


def create_logcat_obj(tag):
    # Initial Logs object from this method
    return Logcat(tag)

if __name__ == '__main__':
    import time
    SYNC_FINISH_PATTERN = "connect"
    logs = create_logcat_obj("HopeBay")
    print "len = " + repr(len(logs.logs))
    print logs.find_until(SYNC_FINISH_PATTERN)
    # print "-" * 40
    # time.sleep(20)
    # isSucc = logs.refresh()
    # print repr(isSucc)
    # print "len = " + repr(len(logs.logs))
    # print repr(logs.logs)
