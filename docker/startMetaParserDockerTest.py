import os

from docker import Docker
import config

logger = config.get_logger().getChild(__name__)

if __name__ == "__main__":
    logger.info("Starting docker")
    repo = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(repo + "/.git"):
        repo = os.path.abspath(os.path.join(repo, os.pardir))
    docker = Docker("test-meta-parser-docker", "docker:5000/docker_hcfs_test_slave", "/bin/sh",
                    "-c /hcfs/tests/functional_test/TestCases/TestMetaParser/start_test_in_docker.sh")
    docker.add_volume((repo, "/hcfs", ""))
    #docker.add_volume(("/dev/bus/usb", "/dev/bus/usb", ""))

    docker.wd = "/hcfs/tests/functional_test/TestCases/TestMetaParser"
    docker.terminate()
    docker.run()
