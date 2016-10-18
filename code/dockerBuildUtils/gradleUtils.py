import subprocess
from subprocess import Popen
from os.path import isfile as fileExists
from os.path import join as pathJoin


RELEASE_APK_RELATIVE = pathJoin(
    "app", "build", "outputs", "apk", "app-release.apk")


def clean(cwd):
    cmd = "./gradlew clean"
    subprocess.call(cmd, shell=True, cwd=cwd)


def build_release(cwd):
    cmd = "./gradlew assembleRelease"
    process = Popen(cmd, shell=True, cwd=cwd)
    out, err = process.communicate()
    release_apk = pathJoin(cwd, RELEASE_APK_RELATIVE)
    if not fileExists(release_apk):
        raise Exception("Fail to build apk:" + str((out, err)))
    return release_apk
