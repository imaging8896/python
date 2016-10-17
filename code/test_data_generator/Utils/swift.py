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
            cmd += " download {0} {1}".format(self._bucket, name)
        elif self._cmd_type == "token" and name:
            cmd += "/{0}".format(name)
        cmd += " -o {0}".format(new_path)
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = process.communicate()
        self.logger.debug("download_file" + repr((cmd, out, err)))
        return out, err

    def download_list_from_marker(self, new_path, marker):
        self.logger.info("Download list from marker")
        cmd = self._cmd_prefix()
        if self._cmd_type == "swift":
            raise Exception("Unsupported.")
        elif self._cmd_type == "token":
            cmd += "/?marker={0}".format(marker)
            cmd += " -o {0}".format(new_path)
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = process.communicate()
        self.logger.debug("download_file" + repr((cmd, out, err)))
        return out, err

    def _cmd_prefix(self):
        if self._cmd_type == "swift":
            return "swift --insecure -A {0} -U {1}:{1} -K {2}".format(self._url, self._user, self._pwd)
        elif self._cmd_type == "token":
            return "curl --insecure -X GET -H \"X-Auth-Token:{0}\" {1}/{2}".format(self._token, self._url, self._bucket)
        raise Exception("Unsupport command type.")
