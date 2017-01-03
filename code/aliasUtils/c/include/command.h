#ifndef TED_COMMAND_H_
#define TED_COMMAND_H_

#include <stdbool.h>

#include "queue.h"

typedef struct CommandExecutor {
	bool (*execute)(struct CommandExecutor* executor);
	void (*free)(struct CommandExecutor* executor);
	void* (*getResult)(struct CommandExecutor* executor);
	void* result;
} CommandExecutor;
typedef CommandExecutor* CommandExecutorPtr;

typedef struct Command {
	bool (*execute)(struct Command* command);
	void (*free)(struct Command* command);
	CommandExecutorPtr executor;
} Command;
typedef Command* CommandPtr;

typedef struct Invoker {
	QueuePtr queue;
	bool (*addCommand)(struct Invoker* invoker, CommandPtr command);
	bool (*execute)(struct Invoker* invoker);
	void (*free)(struct Invoker* invoker);
} Invoker;
typedef Invoker* InvokerPtr;

InvokerPtr newConcurrentInvoker();
InvokerPtr newSingleInvoker();

CommandPtr newCommand(CommandExecutorPtr executor);

CommandExecutorPtr newFullCaseChangeExecutor(char* path);
CommandExecutorPtr newCreateAllAliasExecutor(char* path);
CommandExecutorPtr newCreateFileAliasAndRemoveRepeatExecutor(char* path);

CommandExecutorPtr newGetInosExecutor(char* path, int max);

#endif  /* TED_COMMAND_H_ */
