import subprocess
from subprocess import Popen, PIPE

import config


class Swift(object):
    _token = ""
    _user = ""
    _pwd = ""

    def __init__(self, cmd_type, url, bucket):
        self.logger = config.get_logger().getChild(__name__)
        self._cmd_type = cmd_type
        self._url = url
        self._bucket = bucket

    @classmethod
    def via_token(cls, url, bucket, token):
        swift = cls("token", url, bucket)
        swift._token = token
        return swift

    @classmethod
    def via_swift(cls, user, ip, pwd, bucket):
        swift = cls("swift", "https://" + ip + ":8080/auth/v1.0", bucket)
        swift._user = user
        swift._pwd = pwd
        return swift

    def download_file(self, name, new_path):
        self.logger.info("Download file")
        cmd = self._cmd_prefix()
        if self._cmd_type == "swift":
            cmd += " download " + self._bucket + " " + name + " -o " + new_path
        elif self._cmd_type == "token":
            cmd += "/" + name + " -o " + new_path
        pipe = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = pipe.communicate()
        self.logger.debug("download_file" + repr((cmd, out, err)))
        return out, err

    def _cmd_prefix(self):
        if self._cmd_type == "swift":
            return "swift --insecure -A " + self._url + " -U " + self._user + ":" + self._user + " -K " + self._pwd
        elif self._cmd_type == "token":
            return "curl --insecure -X GET -H \"X-Auth-Token:" + self._token + "\" " + self._url + "/" + self._bucket
        raise Exception("Unsupport command type.")
