import subprocess


def make(cwd, opt=""):
    cmd = "make " + opt
    subprocess.call(cmd, shell=True, cwd=cwd)
