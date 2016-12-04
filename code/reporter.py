from os.path import join as pathJoin

from tedUtils.osUtils import makedirs_if_not_exist, listdir_abs, move_to

"""
log_save_dir
        | -> YYYY-MM-DD-HH-mm-ss
        |                                               |-> log ...
        | -> ...
        | -> latest
                        | -> YYYY-MM-DD-HH-mm-ss
                                                            |-> log ...
"""


class Reporter(object):

    def __init__(self, log_save_dir):
        self.addition_log = []
        self.latest = pathJoin(log_save_dir, "latest")
        makedirs_if_not_exist(self.latest)
        self.move_old_log()
        self.log_save_dir = pathJoin(self.latest, get_new_dirname())
        makedirs_if_not_exist(self.log_save_dir)

    def move_old_log(self):
        latest_parent = pathJoin(self.latest, "..")
        map(move_to(latest_parent), listdir_abs(self.latest))

    def set_log(self, log):
        self.addition_log += [log]

    def add_log(self, log):
        self.addition_log += [log]

    def get_logs(self):
        map(move_to(self.log_save_dir), self.addition_log)


def get_new_dirname():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
