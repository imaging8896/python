from subprocess import Popen
from os.path import isfile as fileExists
from os.path import join as pathJoin


RELEASE_APK_RELATIVE = pathJoin(
    "app", "build", "outputs", "apk", "app-release.apk")


def clean(cwd):
    exec_task("clean", cwd)


def build_release(cwd):
    # _exec_cmd(android update sdk --all  --no-ui --filter
    # extra-android-m2repository", cwd)
    out, err = exec_task("assembleRelease", cwd)
    release_apk = pathJoin(cwd, RELEASE_APK_RELATIVE)
    if not fileExists(release_apk):
        raise Exception("Fail to build apk:" + str((out, err)))
    return release_apk


def exec_task(task, cwd, args=[]):
    cmd = "./gradlew {0} {1}".format(task, " ".join(args))
    return _exec_cmd(cmd, cwd)


def _exec_cmd(cmd, cwd):
    process = Popen(cmd, shell=True, cwd=cwd)
    return process.communicate()
