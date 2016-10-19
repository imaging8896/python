import subprocess
from subprocess import PIPE


def make(cwd, opt=""):
    cmd = "make " + opt
    subprocess.call(cmd, shell=True,  cwd=cwd)

if __name__ == '__main__':
    path = "/home/test/pin/hcfs/tests/functional_test/TestCases/TestMaxPin/TestCases/Utils/hcfsUtils"
    make(path)
