from os.path import join as pathJoin
from os.path import abspath
from os.path import dirname
from shutil import move

from ..docker import docker

DOCKER_BUILD_DIR = "/build_dir"
DOCKER_START_DIR = "/start"

MAKE_SCRIPT = pathJoin(DOCKER_START_DIR, "makeBuild.py")
EXEC_MAKE = "'python {0} {1}'".format(MAKE_SCRIPT, DOCKER_BUILD_DIR)

GRADLE_SCRIPT = pathJoin(DOCKER_START_DIR, "gradleBuildRelease.py")
BUILD_APK_NAME = "test-app.apk"
EXEC_GRADLE = "'python {0} {1} {2}'".format(
    GRADLE_SCRIPT, DOCKER_BUILD_DIR, BUILD_APK_NAME)

THIS_DIR = abspath(dirname(__file__))

# public NDK=bitriseio/android-ndk sdk=ksoichiro/android
# internal NDK=
# NDK:
#   docker:5000/wuxian.zhang/android-ndk-docker (no python)
#   docker:5000/jenkins-terafonn_build-slave
#   ted/ubuntu-ndk-python:14.04-r13b-2.7 (dockerfile)


class AndroidNDKDocker(docker.Docker):

    def __init__(self, name):

        super(AndroidNDKDocker, self).__init__(
            name, "ted/ubuntu-ndk-python:14.04-r13b-2.7", "/bin/sh -c", EXEC_MAKE)
        self.set_privileged()
        self.set_dockerfile_path(THIS_DIR)

        self.add_volume(THIS_DIR, DOCKER_START_DIR, "rw")
        self.set_working_dir(DOCKER_START_DIR)

    def set_build_dir(self, build_dir):
        self.add_volume(build_dir, DOCKER_BUILD_DIR, "rw")


class AndroidSDKDocker(docker.Docker):

    def __init__(self, name):
        super(AndroidSDKDocker, self).__init__(
            name, "docker:5000/android-app-buildbox", "/bin/sh -c", EXEC_GRADLE)
        self.set_privileged()
        self.add_volume(THIS_DIR, DOCKER_START_DIR, "rw")
        self.set_working_dir(DOCKER_START_DIR)
        self.is_finish_build = False

    def set_gradle_proj_dir(self, proj_dir):
        self.proj_dir = proj_dir
        self.add_volume(proj_dir, DOCKER_BUILD_DIR, "rw")

    def run(self):
        super(AndroidSDKDocker, self).run()
        self.is_finish_build = True

    def move_apk_to(self, apk_dest):
        if not self.is_finish_build:
            raise Exception("Get apk before build")
        self.is_finish_build = False
        apk = pathJoin(self.proj_dir, BUILD_APK_NAME)
        move(apk, apk_dest)
