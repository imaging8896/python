import os
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import join as pathJoin

from ..tedUtils.tedUtils import get_cur_timestamp

MEM_TOTAL = "MemTotal"
MEM_FREE = "MemFree"


class AndroidSystemUtils(object):

    def __init__(self, adb):
        self.adb = adb
        self.logger = Logger()
        self.report_dir = self.logger.report_dir

# MemTotal:        1857352 kB
# MemFree:           88700 kB
# Buffers:           28048 kB
# Cached:           975296 kB
# SwapCached:            0 kB
# Active:           747924 kB
# Inactive:         723748 kB
# Active(anon):     470256 kB
# Inactive(anon):      368 kB
# Active(file):     277668 kB
# Inactive(file):   723380 kB
# Unevictable:        1900 kB
# Mlocked:               0 kB
# SwapTotal:             0 kB
# SwapFree:              0 kB
# Dirty:                32 kB
# Writeback:             0 kB
# AnonPages:        470276 kB
# Mapped:           227464 kB
# Shmem:               412 kB
# Slab:              90956 kB
# SReclaimable:      37524 kB
# SUnreclaim:        53432 kB
# KernelStack:       20080 kB
# PageTables:        24244 kB
# NFS_Unstable:          0 kB
# Bounce:                0 kB
# WritebackTmp:          0 kB
# CommitLimit:      928676 kB
# Committed_AS:   45746060 kB
# VmallocTotal:   251658176 kB
# VmallocUsed:       94800 kB
# VmallocChunk:   251487324 kB

    def get_total_mem(self):
        return self.get_memory_info_by_key(MEM_TOTAL)

    def get_free_mem(self):
        return self.get_memory_info_by_key(MEM_FREE)

    def log_mem(self, tag):
        memInfo = self.get_memory_info()
        self.logger.append("{0}\t\t\t: {1}".format(tag, str(memInfo)))

    def get_memory_info_by_key(self, find_key):
        for pairs in self.get_memory_info():
            key, value = pairs.split(":")
            if find_key == key:
                return value.strip()
        raise ValueError("Can't find by key " + find_key)

    def get_memory_info(self):
        cmd = "su 0 cat /proc/meminfo"
        out, err = self.adb.exec_shell(cmd)
        if err:
            raise Exception("Fail to get memory information.")
        return out.split("\r\n")


class Logger(object):

    def __init__(self):
        self.report_dir = pathJoin(abspath(dirname(__file__)), "mem_log")
        if not exists(self.report_dir):
            os.makedirs(self.report_dir)

    def append(self, msg):
        with open(self.get_log_file(), "a") as fout:
            fout.write("{0} : {1}\n".format(get_cur_timestamp(), msg))

    def get_log_file(self):
        if not exists(self.report_dir):
            os.makedirs(self.report_dir)
        return pathJoin(self.report_dir, "memInfo")
