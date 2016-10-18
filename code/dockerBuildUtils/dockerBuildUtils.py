from docker import *


def make_ndk_build(build_dir):
    docker = AndroidNDKDocker("make_ndk_build-docker")
    docker.set_build_dir(build_dir)
    docker.terminate()
    docker.run()


def gradle_build(proj_dir, apk_dest_path):
    docker = AndroidSDKDocker("gradle_build-docker")
    docker.set_gradle_proj_dir(proj_dir)
    docker.terminate()
    docker.run()
    docker.move_apk_to(apk_dest_path)
