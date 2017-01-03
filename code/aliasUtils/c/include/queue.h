#ifndef TED_QUEUE_H_
#define TED_QUEUE_H_

#include <stdbool.h>

typedef struct Queue {
	int (*size)(struct Queue* queue);
	bool (*isEmpty)(struct Queue* queue);
	bool (*isFull)(struct Queue* queue);
	bool (*enQueue)(struct Queue* queue, void* element);
	void* (*deQueue)(struct Queue* queue);
	void (*free)(struct Queue* queue);
} Queue;

typedef Queue* QueuePtr;

QueuePtr newQueue();

#endif  /* TED_QUEUE_H_ */
