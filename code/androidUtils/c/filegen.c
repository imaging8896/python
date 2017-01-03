#include <stdio.h>
#include <stdlib.h>
#include <libgen.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

#include "aliasUtils.h"
#include "utils.h"
#include "command.h"

void outputWhenFailed(bool isSuccess, const char* msg) {
	if(!isSuccess) {
		fprintf(stdout, "error:%s", msg);
		exit(EXIT_FAILURE);
	}
}

int getArgMax(char* arg, char* word) {
	if(!isDigit(arg)) {
		fprintf(stdout, "argument 3 should be 'int' for max alias number");
		exit(EXIT_FAILURE);
	}
	int max = atoi(arg);
	if(max <= 0 || max > getAlphaCaseCombinationNum(word))
		max = getAlphaCaseCombinationNum(word);
	return max;
}

int main(int argc, char **argv)
{
	if(argc < 2)
		goto invalidArgNum;

	char* command = argv[1];
	if(argc == 3) {
		char* path = argv[2];
		if (strcasecmp(command, "allnotexist") == 0) {
			if(!allCaseNotExists(path))
				fprintf(stdout, "%s:exists\n", path);
		} else
			goto invalidArgCommand;
  	} else if(argc == 4) {
		char* path = argv[2];
		char* fileName = strstr(path, basename(path));
		int max = getArgMax(argv[3], fileName);
		if(strcasecmp(command, "getinos") == 0) {
			long* inos = getInos(path, max);
			outputWhenFailed(inos != NULL, strerror(errno));
			for(int i = 0; i < max; i++)
				fprintf(stdout, "%ld\n", inos[i]);
		} else if (strcasecmp(command, "genaliases") == 0)
			outputWhenFailed(genInos(path, max), "fail to generate alias");
		else
			goto invalidArgCommand;
	} else if(argc > 4) {
		if(strcasecmp(command, "concurrent") == 0) {
			// alias concurrent getinos /path1 getinos /path2
			if(argc % 2 == 1)
				goto invalidArgSubCmdNum;
			InvokerPtr invoker = newConcurrentInvoker();
			CommandExecutorPtr commandExecutor;
			char* subCommand;
			char* subComaandPath;
			for(int i = 2; i < argc; i += 2) {
				subCommand = argv[i];
				subComaandPath = argv[i + 1];
				if(strcasecmp(subCommand, "genalias") == 0)
					commandExecutor = newCreateAllAliasExecutor(subComaandPath); 
				else if (strcasecmp(subCommand, "casechange") == 0)
					commandExecutor = newFullCaseChangeExecutor(subComaandPath); 
				else if (strcasecmp(subCommand, "createremove") == 0)
					commandExecutor = newCreateFileAliasAndRemoveRepeatExecutor(subComaandPath); 
				else
					goto invalidArgSubCmd;
				outputWhenFailed(invoker->addCommand(invoker, newCommand(commandExecutor)), "Error whe invoke add command");
			}
			outputWhenFailed(invoker->execute(invoker), "Error whe invoke execute");
		} else
			goto invalidArgCommand;
	} else
		goto invalidArgNum;

	//free all memory
	exit(EXIT_SUCCESS);

invalidArgCommand:
	fprintf(stderr, "Invalid argument command\n");
	goto error;

invalidArgNum:
	fprintf(stdout, "Invalid arguments\n");
	goto error;

invalidArgSubCmdNum:
	fprintf(stdout, "Invalid arguments subcomannd number\n");
	goto error;

invalidArgSubCmd:
	fprintf(stdout, "Invalid arguments subcomannd\n");

error:
	exit(EXIT_FAILURE);
	return 0;
}

