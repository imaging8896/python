from adb import ADB


class ADBCmdWrapper(object):

    def __init__(self, serial_num):
        self.adb = ADB(serial_num)

    def exec_cmd(self, cmd):
        return self.adb.exec_shell("su 0 " + cmd)
