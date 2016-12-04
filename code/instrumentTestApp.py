import os
from os.path import join as pathJoin
from os.path import exists as dirExists

from utilsLib import gradleUtils


class InstrumentTestApp(object):

    def __init__(self, proj):
        self.PROJ_DIR = proj
        set_sdk_env_var()

    def run_instrument_test_package(self, package):
        arg_package = "android.testInstrumentationRunnerArguments.package"
        arg = "-P{0}={1}".format(arg_package, package)
        # connectedCheck
        gradleUtils.exec_task("cC", self.PROJ_DIR, [arg])

    def run_instrument_test_class(self, classes):
        arg_class = "android.testInstrumentationRunnerArguments.class"
        arg = "-P{0}={1}".format(arg_class, classes)
        # connectedCheck
        gradleUtils.exec_task("cC", self.PROJ_DIR, [arg])

    def run_instrument_test_method(self, methods):
        arg_class = "android.testInstrumentationRunnerArguments.class"
        arg = "-P{0}={1}".format(arg_class, methods)
        # connectedCheck
        gradleUtils.exec_task("cC", self.PROJ_DIR, [arg])

    def __str__(self):
        return "project({0})".format(self.PROJ_DIR)


def get_sdk_path():
    env_dict = os.environ
    for key in env_dict:
        for path in env_dict[key].split(":"):
            if dirExists(pathJoin(path, "platforms", "android-23")):
                return path
    # Update sdk?
    raise Exception("Unable to find sdk path")


def set_sdk_env_var():
    sdk = get_sdk_path()
    os.environ["ANDROID_HOME"] = sdk
