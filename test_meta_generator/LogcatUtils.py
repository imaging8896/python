from datetime import datetime
import subprocess
from subprocess import Popen, PIPE
import time


class Logcat(object):
    """
    Logcat format:
    08-15 08:36:43.657  4394  5658 W HopeBay : TeraAPIServer->MgmtApiUtils(run): eventID=1
    08-15 08:36:43.729  4394  4394 D HopeBay : GoogleSignInApiClient(onConnected):

    We parse to [(datetime, type, log), ...] and store it to Logcat object.
    time format : "%m-%d %H:%M:%S.%f"
    """

    def __init__(self, input_tag):
        self.TIME_FMT = "%m-%d %H:%M:%S.%f"
        self.tag = input_tag
        self.logs = self.parse(self.get_raw_logcat())

    def refresh(self, line_num=100):
        new_logs = self.parse(self.get_raw_logcat())
        last_time, _, last_log = self.logs[-1]
        for i, timestamp, _, log in enumerate(new_logs):
            if timestamp == last_time and log == last_log:
                self.logs = new_logs[i:]
                return
        if line_num < 1000:
            self.refresh(line_num + 100)
        else:
            self.logs = new_logs

    def find_until(self, pattern, timeout_sec=300, interval=10):
        for cur_time in [x * interval for x in range(1, timeout_sec / interval)]:
            for timestamp, _, log in reversed(self.logs):
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
        for previous, log in [pair for pair in lines if len(pair) == 2]:
            # 08-15 08:36:43.657  4394  5658 W HopeBay
            pieces = previous.split("  ")  # double space
            if len(pieces) != 3:
                continue
            previous_pieces = [pieces[0], pieces[2]]
            if not self.validate_date(previous_pieces[0]):
                continue
            # 5658 W HopeBay
            pieces = previous_pieces[1].split(" ")  # single space
            if len(pieces) != 3:
                continue
            one_log = (datetime.strptime(previous_pieces[0], self.TIME_FMT),)
            one_log += (pieces[1], log)
            result += [one_log]
        return result

    def get_raw_logcat(self):
        cmd = "adb logcat -d -s " + self.tag
        pipe = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, err = pipe.communicate()
        assert not err, "Error when get raw log string"
        return out

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, self.TIME_FMT)
            return True
        except ValueError as a:
            return False


def create_logcat_obj(tag):
    # Initial Logs object from this method
    return Logcat(tag)

if __name__ == '__main__':
    import time
    SYNC_FINISH_PATTERN = "TeraAPIServer->MgmtApiUtils(run): eventID=2"
    logs = create_logcat_obj("HopeBay")
    print "len = " + repr(len(logs.logs))
    print logs.find_until(SYNC_FINISH_PATTERN)
    # print "-" * 40
    # time.sleep(20)
    # isSucc = logs.refresh()
    # print repr(isSucc)
    # print "len = " + repr(len(logs.logs))
    # print repr(logs.logs)
