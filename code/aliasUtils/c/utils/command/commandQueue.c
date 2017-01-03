#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>

#include "queue.h"
#include "command.h"

#define MAX_SIZE 20
#define EMPTY -1


typedef struct CommandQueue {
	Queue baseQueue;
	int headIndex;
	CommandPtr* array;
} CommandQueue;
typedef CommandQueue* CommandQueuePtr;

static int size(QueuePtr baseQueue) {
	CommandQueuePtr queue = (CommandQueuePtr) baseQueue;
	return queue->headIndex + 1;
}

static bool isEmpty(QueuePtr baseQueue) {
	CommandQueuePtr queue = (CommandQueuePtr) baseQueue;
	return queue->headIndex == EMPTY;
}

static bool isFull(QueuePtr baseQueue) {
	CommandQueuePtr queue = (CommandQueuePtr) baseQueue;
	return queue->headIndex == MAX_SIZE - 1;
}

static bool enQueue(QueuePtr baseQueue, void* element) {
	if(baseQueue->isFull(baseQueue)) {
		errno = ENOMEM;
		return false;
	}
	CommandQueuePtr queue = (CommandQueuePtr) baseQueue;
	queue->array[++queue->headIndex] = (CommandPtr) element;
	return true;
}

static void* deQueue(QueuePtr baseQueue) {
	if(baseQueue->isEmpty(baseQueue)) {
		errno = EPERM;
		return NULL;
	}
	CommandQueuePtr queue = (CommandQueuePtr) baseQueue;
	return queue->array[queue->headIndex--];
}

static void freeQueue(QueuePtr baseQueue) {
	CommandQueuePtr queue = (CommandQueuePtr) baseQueue;
	free(queue->array);
	free(queue);
}

static void initQueue(QueuePtr queue) {
	queue->size = size;
	queue->isEmpty = isEmpty;
	queue->isFull = isFull;
	queue->enQueue = enQueue;
	queue->deQueue = deQueue;
	queue->deQueue = deQueue;
	queue->free = freeQueue;
}

QueuePtr newQueue() {
	CommandQueuePtr queue = malloc(sizeof(CommandQueue));
	initQueue((QueuePtr) queue);
	queue->headIndex = EMPTY;
	queue->array = malloc(sizeof(CommandPtr) * MAX_SIZE);
	return (QueuePtr) queue;
}


