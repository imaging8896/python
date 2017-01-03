#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include <errno.h>

#include "command.h"
#include "queue.h"

void* execCommandJob(void* ptr) {
	CommandPtr command = (CommandPtr) ptr;
	bool isSuccess = command->execute(command);
	command->free(command);
	pthread_exit((isSuccess) ? (void *) 0 : (void *) -1);
}

static bool addCommand(InvokerPtr invoker, CommandPtr command) {
	return invoker->queue->enQueue(invoker->queue, command);
}

static bool execute(InvokerPtr invoker) {
	bool isSuccess = true;
	int commandNum = invoker->queue->size(invoker->queue);
	pthread_t threads[commandNum];
	pthread_attr_t attr;
	pthread_attr_init(&attr);
	int ret;
	//pthread_attr_setstacksize(&attrs, THREADSTACK);

	CommandPtr curCommand;
	for(int i = 0; i < commandNum; i++) {
		curCommand = invoker->queue->deQueue(invoker->queue);
		pthread_create(&threads[i], NULL, execCommandJob, curCommand);
	}
	if(!invoker->queue->isEmpty(invoker->queue)) {
		isSuccess = false;
		goto cleanup;
	}

	for(int i = 0; i <= commandNum; i++) {
		pthread_join(threads[i], (void *)&ret);
		if(ret == -1) {
			isSuccess = false;
			goto cleanup;
		}
	}

cleanup:
	ret = pthread_attr_destroy(&attr);
	if (ret != 0)
		isSuccess = false;
	return isSuccess;
}

static void freeInvoker(InvokerPtr invoker) {
	invoker->queue->free(invoker->queue);
	free(invoker);
}

InvokerPtr newConcurrentInvoker() {
	InvokerPtr invoker = malloc(sizeof(Invoker));
	invoker->queue = newQueue();
	invoker->addCommand = addCommand;
	invoker->execute = execute;
	invoker->free = freeInvoker;
	return invoker;
}
