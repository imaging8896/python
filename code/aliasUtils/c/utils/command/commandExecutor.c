#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <errno.h>

#include "command.h"
#include "aliasUtils.h"
#include "utils.h"

typedef struct AliasCommandExecutor {
	CommandExecutor baseExecutor;
	char* path;
	int max;
} AliasCommandExecutor;
typedef AliasCommandExecutor* AliasCommandExecutorPtr;

static void freeExecutor(CommandExecutorPtr executor) {
	AliasCommandExecutorPtr aliasExecutor = (AliasCommandExecutorPtr) executor;
	free(executor);
}

static bool fullCaseChangeImpl(CommandExecutorPtr executor) {
	AliasCommandExecutorPtr aliasExecutor = (AliasCommandExecutorPtr) executor;
	return fullCaseChange(aliasExecutor->path);
}

CommandExecutorPtr newFullCaseChangeExecutor(char* path) {
	AliasCommandExecutorPtr executor = malloc(sizeof(struct AliasCommandExecutor));
	executor->baseExecutor.free = freeExecutor;
	executor->baseExecutor.execute = fullCaseChangeImpl;
	executor->path = path;
	return (CommandExecutorPtr) executor;
}

static bool createAllAliase(CommandExecutorPtr executor) {
	AliasCommandExecutorPtr aliasExecutor = (AliasCommandExecutorPtr) executor;
	int aliasNum = getAlphaCaseCombinationNum(aliasExecutor->path);
	return genInos(aliasExecutor->path, aliasNum);
}

CommandExecutorPtr newCreateAllAliasExecutor(char* path) {
	AliasCommandExecutorPtr executor = malloc(sizeof(struct AliasCommandExecutor));
	executor->baseExecutor.free = freeExecutor;
	executor->baseExecutor.execute = createAllAliase;
	executor->path = path;
	return (CommandExecutorPtr) executor;
}

static bool createFileAliasAndRemoveRepeat(CommandExecutorPtr executor) {
	AliasCommandExecutorPtr aliasExecutor = (AliasCommandExecutorPtr) executor;
	long* ptr;
	int aliasNum = getAlphaCaseCombinationNum(aliasExecutor->path);
	for(int i = 0; i < 200; i++) {
		FILE *fp = fopen(aliasExecutor->path, "ab+");
		if(!fp)
			return false;
		fclose(fp);
		if(!genInos(aliasExecutor->path, aliasNum))
			return false;
		if(remove(aliasExecutor->path) != 0)
			return false;
		if(access(aliasExecutor->path, F_OK) == 0)
			return false;
	}
	return true;
}

CommandExecutorPtr newCreateFileAliasAndRemoveRepeatExecutor(char* path) {
	AliasCommandExecutorPtr executor = malloc(sizeof(struct AliasCommandExecutor));
	executor->baseExecutor.free = freeExecutor;
	executor->baseExecutor.execute = createFileAliasAndRemoveRepeat;
	executor->path = path;
	return (CommandExecutorPtr) executor;
}

static bool getInosExecutor(CommandExecutorPtr executor) {
	AliasCommandExecutorPtr aliasExecutor = (AliasCommandExecutorPtr) executor;
	executor->result = getInos(aliasExecutor->path, aliasExecutor->max);
	return executor->result != NULL;
}

static void* getResult(CommandExecutorPtr executor) {
	return executor->result;
}

CommandExecutorPtr newGetInosExecutor(char* path, int max) {
	AliasCommandExecutorPtr executor = malloc(sizeof(struct AliasCommandExecutor));
	executor->baseExecutor.free = freeExecutor;
	executor->baseExecutor.execute = getInosExecutor;
	executor->baseExecutor.getResult = getResult;
	executor->path = path;
	executor->max = max;
	return (CommandExecutorPtr) executor;
}

