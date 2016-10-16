#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <pthread.h>

#define workload 2000L
#define THREADSTACK  65536

struct msg {
	long start;
	long end;
};

long size;
const char* test_dir;
const char* content;

void* work(void* ptr) {
	struct msg* msgPtr;
 	msgPtr = (struct msg*) ptr;
	char path[256];
	struct timeval  timeout;
	timeout.tv_sec = 3;    // WAIT seconds
	timeout.tv_usec = 500000;    // 0 milliseconds
	int ready_for_writing = 0;
	fd_set writeFds;

	long i;
	for(i = msgPtr->start; i <= msgPtr->end; i++) {
		snprintf(path, sizeof(path), "%s%s%ld", test_dir, "/", i);
		//int fd = creat(path, 0644);
		int fd = open(path, O_CREAT | O_WRONLY | O_SYNC | O_DSYNC, 0644);
	
		FD_ZERO(&writeFds);
  		FD_SET(fd, &writeFds);
		ready_for_writing = select(1, NULL, &writeFds, NULL, &timeout);
		if (ready_for_writing == -1) { /* Cache full has occured in writing */
        		fprintf(stdout, "select:%d", errno);
			break;
		}
		int ret = write(fd, content, size);
		if(ret == -1) {
			fprintf(stdout, "write:%d", errno);
			break;
		}
    	close(fd);
	}
	pthread_exit((void *) 0);
}

void prepare_random_content() {
	char* random = (char *)malloc(1024 * 1024 * sizeof(char));
	FILE *f = fopen("/data/random", "rb");
	fseek(f, 0, SEEK_END);
	long fsize = ftell(f);
	fseek(f, 0, SEEK_SET);  //same as rewind(f);
	fread(random, fsize, 1, f);
	fclose(f);

	if(size <= 1024 * 1024) {
		content = random;
	} else if(size > 1024 * 1024) {
		char* extend_random = (char *)malloc(size);
		int times = size / (1024 * 1024);
		int rest = size - (1024 * 1024 * times);
		char* ptr;
		ptr = extend_random;
		int i;
		for(i = 0; i < times; i++) {
			memcpy (ptr, random, 1024 * 1024 * sizeof(char));
			ptr = ptr + sizeof(random);
		}
		memcpy (ptr, random, rest * sizeof(char));
		content = extend_random;
	}
}

int main(int argc, char **argv)
{
	char* ptr;
	long num = strtol(argv[1], &ptr, 10);
	size = strtol(argv[2], &ptr, 10);
	test_dir = argv[3];

	prepare_random_content();
		
	long round = num / workload;
	pthread_t threads[round + 1];
	long last = num % workload;

	pthread_attr_t  attrs;
	pthread_attr_init(&attrs);
	pthread_attr_setstacksize(&attrs, THREADSTACK);
	
	long i;
	for(i = 0; i <= round; i++) {
		struct msg* msgPtr = malloc(sizeof(struct msg));
		msgPtr->start = workload * i + 1L;
		if(i == round)
			msgPtr->end = last;
		else
			msgPtr->end = workload * i + workload;//&attrs
		pthread_create(&threads[i], NULL, work, (void*) msgPtr);
	}
	for(i = 0; i <= round; i++) {
		pthread_join(threads[i], NULL);
	}
    return 0;
}

