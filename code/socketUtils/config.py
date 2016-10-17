import os
import logging
import ConfigParser


class Config(object):

    def __init__(self):
        config = ConfigParser.ConfigParser()
        this_dir = os.path.abspath(os.path.dirname(__file__))
        config.read(os.path.join(this_dir, "config.ini"))
        self.log_level = int(config.get("Global", "log_level"))


def get_logger():
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(Config().log_level)
    return logger

if __name__ == '__main__':
    print Config().log_level
