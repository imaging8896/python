from datetime import datetime
import subprocess
from subprocess import Popen, PIPE
import time

import adb


class HCFSLog(object):
    """
    HCFS LOG format:
    2016-07-26 10:39:06.985782\tDebug: sync paused. pinning manager takes a break
    2016-07-26 10:39:07.183878\tChecking cache size 1391750822, 8237418240

    We parse to [(datetime, log), ...] and store it to HCFSLog object.
    time format : "%Y-%m-%d %H:%M:%S.%f"
    """

    def __init__(self):
        self.TIME_FMT = "%Y-%m-%d %H:%M:%S.%f"
        self.logs = self.parse(self.get_raw_log())

    def refresh(self, line_num=100):
        new_logs = self.parse(self.get_raw_log(line_num))
        last_time, last_log = self.logs[-1]
        i = 0
        for timestamp, log in new_logs:
            if timestamp == last_time and log == last_log:
                break
            i += 1
        if(i == len(new_logs)):
            line_num += 100
            if line_num < 1000:
                self.refresh(line_num)
            else:
                self.logs = new_logs
        else:
            self.logs.extend(new_logs[(i + 1):len(new_logs)])

    def find_until(self, pattern, timeout_sec=300):
        # cur_logs = [log for i, log in enumerate(self.logs) if i >= self.cur_i]
        # Find pattern in log from now until timeout
        self.refresh()
        now = datetime.now()
        cur_time = 0
        while cur_time < timeout_sec:
            cur_logs = [(timestamp, log)
                        for timestamp, log in self.logs if timestamp > now]
            for timestamp, log in cur_logs:
                if pattern in log:
                    return True, timestamp, log
            time.sleep(10)
            self.refresh()
            cur_time += 10
        return False, None, None

    def parse(self, logs_str):
        # parse to [(datetime object, log string), ...]
        # Seperate by line
        lines = logs_str.split("\r\n")
        # Seperate by "tab". Keep log which the format matches "time'/t'log"
        lines = [tuple(line.split("\t")) for line in lines if line]
        lines = [pair for pair in lines if len(pair) == 2]
        # Formate time to datetime object
        lines = [(datetime.strptime(timestamp, self.TIME_FMT), log)
                 for timestamp, log in lines if self.validate_date(timestamp)]
        # Filter wrong date time log
        #(Some logs has time 1970-01-26 21:26:39.078667)
        return [(timestamp, log)
                for timestamp, log in lines if timestamp > datetime(2016, 1, 1)]

    def get_raw_log(self, line_num=100):
        cmd = "tail -n" + str(line_num) + " /data/hcfs_android_log "
        out, err = adb.exec_cmd(cmd)
        assert not err, "Error when get raw log string"
        return out

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, self.TIME_FMT)
            return True
        except ValueError:
            return False


def create_HCFS_log_obj():
    # Initial Logs object from this method
    return HCFSLog()

if __name__ == '__main__':
    import time

    logs = create_HCFS_log_obj()
    print "len = " + repr(len(logs.logs))
    print repr(logs.logs)
    print "-" * 40
    time.sleep(20)
    isSucc = logs.refresh()
    print repr(isSucc)
    print "len = " + repr(len(logs.logs))
    print repr(logs.logs)
