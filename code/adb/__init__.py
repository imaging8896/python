from adb import ADB


def get_device_serial_num():
    import ConfigParser
    from os.path import abspath
    from os.path import dirname
    from os.path import join as pathJoin

    config = ConfigParser.ConfigParser()
    this_dir = abspath(dirname(__file__))
    config.read(pathJoin(this_dir, "device.ini"))
    serial_num = config.get("one_device", "serial_num")
    return serial_num if serial_num else None


serial_num = get_device_serial_num()
adb = ADB(serial_num)
