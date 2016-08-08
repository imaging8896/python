import logging
import os


class Config(object):

    def __init__(self):
        self.init_from_config_file()

    def init_from_config_file(self):
        this_dir = os.path.abspath(os.path.dirname(__file__))
        with open(this_dir + "/config.ini", "rt") as fin:
            for line in fin:
                line = line.strip()
                if line.startswith("#"):
                    continue
                key = line.split("=")[0]
                value = line.split("=")[1]
                if key == "log_level":
                    self.log_level = int(value)


def get_logger():
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(Config().log_level)
    return logger
