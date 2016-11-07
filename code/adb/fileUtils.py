import os

from wrapper import ADBCmdWrapper


class AndroidFileUtils(object):

    def __init__(self, serial_num):
        self.cmd_wrapper = ADBCmdWrapper(serial_num)

    def touch(self, path):
        cmd = "touch {0}".format(path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def dd_bs_1m(self, path, count, in_stream, opt=""):
        cmd = "dd if={0} of={1} bs=1048576 count={2} {3}".format(
            in_stream, path, str(count), opt)
        return self.cmd_wrapper.exec_cmd(cmd)

    def dd_one_count(self, path, size, in_stream, opt=""):
        cmd = "dd if={0} of={1} bs={2} count=1 {3}".format(
            in_stream, path, str(size), opt)
        return self.cmd_wrapper.exec_cmd(cmd)

    def dd(self, path, bs, count, in_stream, opt=""):
        cmd = "dd if={0} of={1} bs={2} count={3} {4}".format(
            in_stream, path, str(bs), str(count), opt)
        return self.cmd_wrapper.exec_cmd(cmd)

    def rm(self, path):
        cmd = "rm -f {0}".format(path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def rm_r(self, path):
        cmd = "rm -rf {0}".format(path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def rmdir(self, path):
        cmd = "rmdir {0}".format(path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def mv(self, src_path, dest_path):
        cmd = "mv {0} {1}".format(src_path, dest_path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def append(self, content, path):
        cmd = "'echo \"{0}\" >> {1}'".format(content, path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def empty_file(self, file):
        cmd = "'echo -n > {}'".format(file)
        return self.cmd_wrapper.exec_cmd(cmd)

    def read(self, path):
        cmd = "'cat {0}'".format(path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def mkdir(self, path):
        cmd = "'mkdir {0}'".format(path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def makedirs(self, path):
        if not self.is_existed(path):
            self.makedirs(os.path.dirname(path))
            self.mkdir(path)

    def ls(self, path, opt=""):
        cmd = "'ls {0} {1}'".format(opt, path)
        return self.cmd_wrapper.exec_cmd(cmd)

    def is_existed(self, path):
        ls_result, err = self.ls(path)
        if err:
            raise Exception("Error while 'ls' {0}".format(path))
        return ("No such file" not in ls_result)

    def get_ino(self, path):
        out = self.stat("i", path)
        if not out.isdigit():
            raise ValueError("Stat inode number not digit <{0}>".format(out))
        return int(out)

    def get_file_name(self, path, ino):
        out, _ = self.ls(path, "-i")
        ino_name_pairs = out.rstrip().split("\r\n")
        for ino_name_pair in ino_name_pairs:
            file_ino, file_name = ino_name_pair.lstrip().split(" ")
            if int(file_ino) == ino:
                return file_name
        raise Exception("{0} is not found in {1}".format(ino, path))

    def get_file_stat(self, path):
        result_list = self.stat_all(path)
        stat = {}
        stat["access_right"] = result_list[0]
        stat["access_right_rwz"] = result_list[1]
        stat["block_num"] = result_list[2]
        stat["block_size"] = result_list[3]
        stat["device_id"] = result_list[4]  # endswith "d"
        stat["device_id_hex"] = result_list[5]  # endswith "h"
        stat["mode"] = result_list[6]
        stat["file_type"] = result_list[7]
        stat["gid"] = result_list[8]  # group ID of owner
        stat["group_name"] = result_list[9]  # group name of owner
        stat["hard_link_num"] = result_list[10]
        stat["ino"] = result_list[11]
        stat["io_block_size"] = result_list[12]
        stat["size"] = result_list[13]
        stat["uid"] = result_list[14]  # user ID of owner
        stat["user_name"] = result_list[15]  # user name of owner
        stat["atime"] = result_list[16]  # access time (need???)
        stat["file_write_time"] = result_list[17]
        stat["dir_change_time"] = result_list[18]
        return stat

    def stat_all(self, path, remove_opts=None):
        # %a  Access bits (octal) |%A  Access bits (flags)|%b  Blocks allocated
        # %B  Bytes per block     |%d  Device ID (dec)    |%D  Device ID (hex)
        # %f  All mode bits (hex) |%F  File type          |%g  Group ID
        # %G  Group name          |%h  Hard links         |%i  Inode
        # %n  Filename            |%N  Long filename      |%o  I/O block size
        # %s  Size (bytes)        |%u  User ID            |%U  User name
        # %x  Access time         |%X  Access unix time   |%y  File write time
        # %Y  File write unix time|%z  Dir change time    |%Z  Dir change unix time
        # disable %n %N, because it's just input path
        opt = ["a", "A", "b", "B", "d", "D",
               "f", "F", "g", "G", "h", "i",
               "o", "s", "u", "U", "X", "Y", "Z"]
        if remove_opts:
            for remove_opt in remove_opts:
                opt.remove(remove_opt)
        cmd = "stat -c%{0} {1}".format(",%".join(opt), path)
        out, err = self.cmd_wrapper.exec_cmd(cmd)
        if err:
            raise Exception("Stat <" + path + "> error:" + err)
        stat = out.rstrip().split(",")
        if len(stat) != len(opt):
            raise Exception(
                "Stat <{0}> has problem stat result =({1})".format(path, out))
        return stat

    def stat(self, opt, path):
        cmd = "stat -c%{0} {1}".format(opt, path)
        out, err = self.cmd_wrapper.exec_cmd(cmd)
        if err:
            raise Exception("Stat <" + path + "> error:" + err)
        if not out:
            raise Exception("Stat <" + path + "> result is empty")
        return out.rstrip()

if __name__ == '__main__':
    # file_utils = FileUtils()
    # print file_utils.get_file_stat("/home/test")
    file_utils = FileUtils(wrapper.ADBCmdWrapper("Ted"))
    print file_utils.get_file_stat("/storage/emulated/0/1.f")
    file_utils.makedirs("/storage/emulated/0/a/b/c/d")
    print file_utils.is_existed("/storage/emulated/0/a/b/c/d")
    print file_utils.ls("/storage/emulated/0/a/b/c/d")
    file_utils.rm_r("/storage/emulated/0/a")
