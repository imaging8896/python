import os

from wrapper import ADBCmdWrapper

MEM_TOTAL = "MemTotal"
MEM_FREE = "MemFree"


class AndroidSystemUtils(object):

    def __init__(self, serial_num):
        self.cmd_wrapper = ADBCmdWrapper(serial_num)

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
        return self.get_memory(MEM_TOTAL)

    def get_free_mem(self):
        return self.get_memory(MEM_FREE)

    def get_memory(self, key):
        cmd = "cat /proc/meminfo | grep " + key
        out, err = self.cmd_wrapper.exec_cmd(cmd)
        if err:
            raise Exception("Fail to get memory information.")
        find_key, value = out.split(":")
        if find_key != key:
            raise ValueError("Can't find by key " + key)
        return value.strip()


if __name__ == '__main__':
    # file_utils = FileUtils()
    # print file_utils.get_file_stat("/home/test")
    import wrapper
    sys_utils = SystemUtils(wrapper.ADBCmdWrapper("Ted"))
    print sys_utils.get_memory(MEM_TOTAL)
    print sys_utils.get_memory(MEM_FREE)
