# Any object which wants to run on docker, must inherit from Dockerable
import os
import config
from docker import Docker


class AdbDocker(Docker):

    def __init__(self, name, image, shell_cmd, shell_args):
        super(AdbDocker, self).__init__(name, image, shell_cmd, shell_args)
        self.add_volume("/dev/bus/usb", "/dev/bus/usb", "rw")
        self.set_privileged()
