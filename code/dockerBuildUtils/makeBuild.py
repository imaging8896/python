import os
from os.path import exists as dirExists
from os.path import isfile as fileExists
from os.path import join as pathJoin
import sys

from utilsLib import makeUtils

MAKEFILE_NDK_ENV_VAR = "ANDROID_NDK"


def is_ndk_has_platform(ndk_path, android_api_ver, cpu_arch):
    platform = pathJoin(ndk_path, "platforms", android_api_ver, cpu_arch)
    return dirExists(platform)


def is_ndk_has_gcc(ndk_path, arch, os, gcc):
    gcc = pathJoin(ndk_path, "toolchains", arch, "prebuilt", os, "bin", gcc)
    return fileExists(gcc)


def check_ndk_version(ndk_path):
    if not is_ndk_has_platform(ndk_path, "android-21", "arch-arm64") or not is_ndk_has_gcc(ndk_path, "aarch64-linux-android-4.9", "linux-x86_64", "aarch64-linux-android-gcc"):
        raise Exception("Invalid ndk version")


def get_ndk_path():
    env_dict = os.environ
    for key in env_dict:
        for path in env_dict[key].split(":"):
            if fileExists(pathJoin(path, "ndk-build")):
                return path
    raise Exception("Unable to find ndk path")


def set_ndk_env_var():
    ndk = get_ndk_path()
    check_ndk_version(ndk)
    os.environ[MAKEFILE_NDK_ENV_VAR] = ndk


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Invalid argument number need 1 but " + str(sys.argv))
    set_ndk_env_var()
    # make gen file permission free
    os.umask(000)
    makeUtils.make(sys.argv[1], "clean")
    makeUtils.make(sys.argv[1])
