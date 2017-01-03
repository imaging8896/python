#include <stdlib.h>

#include "command.h"

static bool execute(CommandPtr command) {
	return command->executor->execute(command->executor);
}

static void freeCommand(CommandPtr command) {
	command->executor->free(command->executor);
	free(command);
}

struct ConcreteCommand {
	Command command;
	CommandExecutorPtr executor;
};

CommandPtr newCommand(CommandExecutorPtr executor) {
	CommandPtr command = malloc(sizeof(Command));
	command->execute = execute;
	command->free = freeCommand;
	command->executor = executor;
	return command;
}
