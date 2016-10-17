import ConfigParser
import os

from adb import ADB
from activityManager import ActivityManager
import fileUtils

__all__ = ["serial_num", "adb", "android_fileUtils", "am"]

config = ConfigParser.ConfigParser()
this_dir = os.path.abspath(os.path.dirname(__file__))
config.read(os.path.join(this_dir, "device.ini"))

serial_num = config.get("one_device", "serial_num")
serial_num = serial_num if serial_num else None
adb = ADB(serial_num)
android_fileUtils = fileUtils.AndroidFileUtils(serial_num)
am = ActivityManager(serial_num)
