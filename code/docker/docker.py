import os
import subprocess

import config


class Docker(object):

    def __init__(self, name, image, shell_cmd, shell_args):
        if not os.path.exists("/var/run/docker.sock"):
            raise EnvironmentError("Need installed docker.")
        self.logger = config.get_logger().getChild(__name__)
        self.docker_cmd = "docker run --rm"
        self.add_volume("/etc/localtime", "/etc/localtime", "ro")
        self.set_tty()

        self.name = name
        self.image = image
        self.shell_cmd = shell_cmd
        self.shell_args = shell_args

    def add_volume(self, host_vol, cont_vol, permission=""):
        self.logger.info("add_volume" + repr((host_vol, cont_vol, permission)))
        vol_opt = "{0}:{1}:{2}".format(
            host_vol, cont_vol, permission).strip(":")
        self.docker_cmd += " -v " + vol_opt

    def set_privileged(self):
        self.logger.info("set_privileged")
        self.docker_cmd += " --privileged"

    # TODO default set, HOW to disable
    def set_tty(self):
        self.logger.info("set_tty")
        self.docker_cmd += " -t"

    def set_interactive(self):
        self.logger.info("set_interactive")
        self.docker_cmd += " -i"

    def set_working_dir(self, path):
        self.logger.info("set_working_dir " + path)
        self.docker_cmd += " -w " + path

    def run(self):
        try:
            self.logger.info("Run docker " + self.name)
            cmd = "{0} --name={1} {2} {3} {4}".format(
                self.docker_cmd, self.name, self.image, self.shell_cmd, self.shell_args)
            self.logger.info("run" + repr((cmd)))
            subprocess.call(cmd, shell=True)
        except Exception as e:
            self.cleanup()
            print e

    def terminate(self):
        self.logger.info("Terminate docker " + self.name)
        cmd = "sudo docker rm -f " + self.name
        subprocess.call(cmd, shell=True)
        self.logger.debug("terminate" + repr((cmd)))

    def cleanup(self):
        self.logger.info("cleanup " + self.name)
        self.terminate()
