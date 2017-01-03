#include <stdlib.h>
#include <stdbool.h>

#include "command.h"
#include "queue.h"

static bool addCommand(InvokerPtr invoker, CommandPtr command) {
	return invoker->queue->enQueue(invoker->queue, command);
}

static bool execute(InvokerPtr invoker) {
	int commandNum = invoker->queue->size(invoker->queue);
	CommandPtr curCommand;
	for(int i = 0; i < commandNum; i++) {
		curCommand = invoker->queue->deQueue(invoker->queue);
		if(!curCommand->execute(curCommand))
			return false;
	}
	return true;
}

static void freeInvoker(InvokerPtr invoker) {
	invoker->queue->free(invoker->queue);
	free(invoker);
}

InvokerPtr newSingleInvoker() {
	InvokerPtr invoker = malloc(sizeof(Invoker));
	invoker->queue = newQueue();
	invoker->addCommand = addCommand;
	invoker->execute = execute;
	invoker->free = freeInvoker;
	return invoker;
}
