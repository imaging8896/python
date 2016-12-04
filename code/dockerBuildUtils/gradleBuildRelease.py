import os
from os.path import exists as dirExists
from os.path import join as pathJoin
import sys
from shutil import move, rmtree

from utilsLib import gradleUtils


def get_sdk_path():
    env_dict = os.environ
    for key in env_dict:
        for path in env_dict[key].split(":"):
            if dirExists(pathJoin(path, "platforms", "android-23")):
                return path
    raise Exception("Unable to find sdk path")


def set_sdk_env_var():
    sdk = get_sdk_path()
    os.environ["ANDROID_HOME"] = sdk


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Invalid argument number need 2 but " + str(sys.argv))
    set_sdk_env_var()
    build_path = sys.argv[1]
    apk_dest_path = sys.argv[2]
    gradleUtils.clean(build_path)
    apk = gradleUtils.build_release(build_path)
    os.chdir(build_path)
    move(apk, apk_dest_path)
    gradleUtils.clean(build_path)
    # remove .gradle to prevent permission denied while remove .gradle
    gradle_tmp = pathJoin(build_path, ".gradle")
    if dirExists(gradle_tmp):
        rmtree(gradle_tmp)
