# Any object which wants to run on docker, must inherit from Dockerable
import os
import subprocess
from subprocess import Popen, PIPE

import config

logger = config.get_logger().getChild(__name__)


class Docker(object):

    # volume:[(str,str,str) ...] =>(host src), dest, (options)
    def __init__(self, name, image, cmd, args):
        if not os.path.exists("/var/run/docker.sock"):
            raise EnvironmentError("Need installed docker.")
        self.name = name
        self.volume = [("/etc/localtime", "/etc/localtime", "ro")]
        self.image = image
        self.cmd = cmd
        self.args = args
        self.tty = True
        self.wd = ""
        self.logger = config.get_logger().getChild(__name__)

    def add_volume(self, vol):
        self.logger.info("Add volume")
        self.logger.debug("add_volume" + repr((vol)))
        if not isinstance(vol, tuple):
            raise TypeError("Input need 'tuple")
        if len(vol) != 3:
            raise ValueError("Input need '3 element' tuple")
        if not vol[1]:
            raise ValueError(
                "second element (destnation source) shouldn't be empty")
        self.volume.extend([vol])

    def get_run_cmd(self):
        cmd = ["docker run --rm "]
        cmd.extend(["-t" if self.tty else ""])
        cmd.extend(["--name=" + self.name])
        for (hsrc, dsrc, opt) in self.volume:
            vol = (hsrc + ":") if hsrc else ""
            vol = vol + dsrc
            vol = vol + ((":" + opt) if opt else "")
            cmd.extend(["-v", vol])
        if self.wd:
            cmd.extend(["-w", self.wd])
        cmd.extend([self.image, self.cmd, self.args])
        return " ".join(cmd)

    def run(self):
        try:
            logger.info("Run docker " + self.name)
            cmd = self.get_run_cmd()
            subprocess.call(cmd, shell=True)
            logger.debug("run" + repr((cmd)))
        except Exception as e:
            self.cleanup()
            print e

    def terminate(self):
        logger.info("Terminate docker " + self.name)
        cmd = "sudo docker rm -f " + self.name
        subprocess.call(cmd, shell=True)
        logger.debug("terminate" + repr((cmd)))

    def cleanup(self):
        logger.info("cleanup " + self.name)
        self.terminate()
