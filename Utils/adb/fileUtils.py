from adb import ADB
from .. import fileUtils


class ADBCmdWrapper(object):

    def __init__(self, serial_num):
        self.adb = ADB(serial_num)

    def exec_cmd(self, cmd):
        return self.adb.exec_shell("su 0 " + cmd)


class AndroidFileUtils(fileUtils.FileUtils):

    def __init__(self, serial_num):
        super(AndroidFileUtils, self).__init__(ADBCmdWrapper(serial_num))
