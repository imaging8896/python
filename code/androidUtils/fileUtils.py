from os.path import dirname
from os.path import basename


class AndroidFileUtils(object):

    def __init__(self, adb):
        self.adb = adb

    def touch(self, path):
        cmd = "su 0 touch {0}".format(path)
        return self.adb.exec_shell(cmd)

    def cp(self, src, dest):
        cmd = "su 0 cp {0} {1}".format(src, dest)
        return self.adb.exec_shell(cmd)

    def dd_bs_1m(self, path, count, in_stream, opt=""):
        cmd = "su 0 dd if={0} of={1} bs=1048576 count={2} {3}".format(
            in_stream, path, str(count), opt)
        return self.adb.exec_shell(cmd)

    def dd_one_count(self, path, size, in_stream, opt=""):
        cmd = "su 0 dd if={0} of={1} bs={2} count=1 {3}".format(
            in_stream, path, str(size), opt)
        return self.adb.exec_shell(cmd)

    def dd(self, path, bs, count, in_stream, opt=""):
        cmd = "su 0 dd if={0} of={1} bs={2} count={3} {4}".format(
            in_stream, path, str(bs), str(count), opt)
        return self.adb.exec_shell(cmd)

    def rm(self, path):
        cmd = "su 0 rm -f {0}".format(path)
        return self.adb.exec_shell(cmd)

    def rm_r(self, path):
        cmd = "su 0 rm -rf {0}".format(path)
        return self.adb.exec_shell(cmd)

    def rmdir(self, path):
        cmd = "su 0 rmdir {0}".format(path)
        return self.adb.exec_shell(cmd)

    def mv(self, src_path, dest_path):
        cmd = "su 0 mv {0} {1}".format(src_path, dest_path)
        return self.adb.exec_shell(cmd)

    def append(self, content, path):
        cmd = "'su 0 echo \"{0}\" >> {1}'".format(content, path)
        return self.adb.exec_shell(cmd)

    def empty_file(self, file):
        cmd = "'su 0 echo -n > {}'".format(file)
        return self.adb.exec_shell(cmd)

    def read(self, path):
        cmd = "'su 0 cat {0}'".format(path)
        return self.adb.exec_shell(cmd)

    def mkdir(self, path):
        cmd = "'su 0 mkdir {0}'".format(path)
        return self.adb.exec_shell(cmd)

    def makedirs(self, path):
        if not self.is_existed(path):
            self.makedirs(dirname(path))
            self.mkdir(path)

    def ls(self, path, opt=""):
        cmd = "'su 0 ls {0} {1}'".format(opt, path)
        return self.adb.exec_shell(cmd)

    def is_existed(self, path):
        ls_result, err = self.ls(path)
        if err:
            raise Exception("Error while 'ls' {0}".format(path))
        return ("No such file" not in ls_result)

    def get_all_files(self, path):
        cmd = "'su 0 find {} -type f'".format(path)
        return self.adb.exec_shell(cmd)[0].split("\r\n")

    def get_all_file_names(self, path):
        return map(basename, self.get_all_files(path))

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
        cmd = "su 0 stat -c%{0} {1}".format(",%".join(opt), path)
        out, err = self.adb.exec_shell(cmd)
        if err:
            raise Exception("Stat <" + path + "> error:" + err)
        stat = out.rstrip().split(",")
        if len(stat) != len(opt):
            raise Exception(
                "Stat <{0}> has problem stat result =({1})".format(path, out))
        return stat

    def stat(self, opt, path):
        cmd = "su 0 stat -c%{0} {1}".format(opt, path)
        out, err = self.adb.exec_shell(cmd)
        if err:
            raise Exception("Stat <" + path + "> error:" + err)
        if not out:
            raise Exception("Stat <" + path + "> result is empty")
        return out.rstrip()


if __name__ == '__main__':
    from __init__ import adb
    # file_utils = FileUtils()
    # print file_utils.get_file_stat("/home/test")
    file_utils = AndroidFileUtils(adb)
    print file_utils.get_file_stat("/storage/emulated/0/1.f")
    file_utils.makedirs("/storage/emulated/0/a/b/c/d")
    print file_utils.is_existed("/storage/emulated/0/a/b/c/d")
    print file_utils.ls("/storage/emulated/0/a/b/c/d")
    file_utils.rm_r("/storage/emulated/0/a")
