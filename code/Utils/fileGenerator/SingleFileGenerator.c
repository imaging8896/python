#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

long size;
const char* file_path;
const char* content;

void write_file() {
	int fd = open(file_path, O_CREAT | O_WRONLY | O_SYNC | O_DSYNC, 0644);
	int times = size / (1024 * 1024);
	int rest = size - (times * 1024 * 1024);
	int i;
	for(i = 0; i < times; i++) {
		int ret = write(fd, content, 1024 * 1024 * sizeof(char));
		if(ret == -1) {
			fprintf(stdout, "write:%d", errno);
			goto finally;
		}
	}
	int ret = write(fd, content, rest * sizeof(char));
	if(ret == -1) {
		fprintf(stdout, "write:%d", errno);
		goto finally;
	}

finally:
    close(fd);
}

void prepare_random_content() {
	char* random = (char *)malloc(1024 * 1024 * sizeof(char));
	FILE *f = fopen("/data/random", "rb");
	fseek(f, 0, SEEK_END);
	long fsize = ftell(f);
	fseek(f, 0, SEEK_SET);  //same as rewind(f);
	fread(random, fsize, 1, f);
	fclose(f);

	content = random;
}

int main(int argc, char **argv)
{
	char* ptr;
	file_path = argv[1];
	size = strtol(argv[2], &ptr, 10);

	prepare_random_content();
	write_file();
    return 0;
}

