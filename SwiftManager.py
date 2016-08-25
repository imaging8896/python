import subprocess
from subprocess import Popen, PIPE

import config


class Swift(object):

    def __init__(self, user, ip, pwd, bucket):
        self._user = user
        self._ip = ip
        self._url = "https://" + ip + ":8080/auth/v1.0"
        self._pwd = pwd
        self._bucket = bucket
        self._useDocker = False
        self.logger = config.get_logger().getChild(__name__)

    @classmethod
    def fromDocker(cls, docker, user, pwd, bucket):
        swift = cls(user, docker.getIP(), pwd, bucket)
        swift._useDocker = True
        return swift

    def cleanup(self):
        self.logger.info("cleanup")
        if not self._useDocker:
            self.rm_bucket()

    def rm_bucket(self):
        self.logger.info("Remove bucket")
        cmd = self._cmd_prefix()
        cmd.extend(["delete", self._bucket])
        subprocess.call(" ".join(cmd), shell=True, stdout=PIPE, stderr=PIPE)
        self.logger.debug("rm_bucket" + repr((" ".join(cmd))))

    def create_bucket(self):
        self.logger.info("Create bucket")
        cmd = self._cmd_prefix()
        cmd.extend(["post", self._bucket])
        subprocess.call(" ".join(cmd), shell=True, stdout=PIPE, stderr=PIPE)
        self.logger.debug("create_bucket" + repr((" ".join(cmd))))

    def check_bucket(self):
        self.logger.info("Check bucket")
        cmd = self._cmd_prefix()
        cmd.extend(["list", self._bucket])
        pipe = subprocess.Popen(
            " ".join(cmd), stdout=PIPE, stderr=PIPE, shell=True)
        out, err = pipe.communicate()
        self.logger.debug("check_bucket" + repr((" ".join(cmd), out, err)))
        assert not err, err

    def download_file(self, name, new_path_name):
        self.logger.info("Download file")
        cmd = self._cmd_prefix()
        cmd.extend(["download", self._bucket, name, "-o", new_path_name])
        pipe = subprocess.Popen(
            " ".join(cmd), stdout=PIPE, stderr=PIPE, shell=True)
        out, err = pipe.communicate()
        self.logger.debug("download_file" + repr((" ".join(cmd), out, err)))
        assert not err, err

    def _cmd_prefix(self):
        return ["swift --insecure -A", self._url, "-U", self._user + ":" + self._user, "-K", self._pwd]
