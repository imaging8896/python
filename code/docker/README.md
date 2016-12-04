docker.py 為以 python 呼叫 docker 指令, startMetaParserDockerTest.py 設定 meta_parser 測試的 docker 環境參數.

範例 "Dockerfile"

Ex 1 (execute cmd and exit):

- from docker import Docker
- docker = Docker("dockerInstanceName1", "dockerImageName:dockerTag", "/bin/sh -c ", "echo 'hello world'")
- docker.set_dockerfile_path("/path/to/dockerfile")
- docker.add_volume("/some/abs/path", "/abs/path/in/docker", "rw")
- docker.set_working_dir("/working/directory/when/run/in/docker")
- docker.terminate()
- docker.run()

Ex 2 (interactive) :

- from docker import Docker
- docker = Docker("dockerInstanceName2", "dockerImageName:dockerTag", "/bin/bash", "")
- docker.set_dockerfile_path("/path/to/dockerfile")
- docker.set_interactive()
- docker.add_volume("/some/abs/path", "/abs/path/in/docker", "rw")
- docker.set_working_dir("/working/directory/when/run/in/docker")
- docker.terminate()
- docker.run()
