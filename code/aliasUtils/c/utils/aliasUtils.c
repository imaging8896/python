#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <libgen.h>
#include <ctype.h>

#include "aliasUtils.h"
#include "utils.h"

long* getInos(char* path, int max) {
	if(path == NULL || max <= 0 || max > getAlphaCaseCombinationNum(path)) {
		errno = EPERM;
		return NULL;
	}

	long* inos = (long *) malloc(sizeof(long) * max);
	char* fileName = strstr(path, basename(path));
	int allCombinationNum = getCaseCombinationNum(fileName);
	int i = 0;
	for(int bitmap = 0; bitmap < allCombinationNum; bitmap++) {
		if(setCombination(fileName, bitmap)) {
			long ino = getIno(path);
			if(ino == -1) {
				free(inos);
				return NULL;
			}
			inos[i++] = ino;
		}
		if(i == max)
			break;
	}
	return inos;
}

bool genInos(char* path, int max) {
	long* ptr = getInos(path, max);
	if(ptr != NULL)
		free(ptr);
	return ptr != NULL;
}

bool fullCaseChange(char* path) {
	char* fileName = strstr(path, basename(path));
	char curPath[strlen(path) + 1];
	strncpy(curPath, path, strlen(path) + 1);
	int allCombinationNum = getCaseCombinationNum(fileName);
	int i = 0;
	for(int bitmap = 0; bitmap < allCombinationNum; bitmap++) {
		if(setCombination(fileName, bitmap)) {
			if(rename(curPath, path) != 0)
				return false;
			strncpy(curPath, path, strlen(path) + 1);
		}
	}
	return true;
}

bool allCaseNotExists(char* path) {
	char* fileName = strstr(path, basename(path));
	int allCombinationNum = getCaseCombinationNum(fileName);
	for(int bitmap = 0; bitmap < allCombinationNum; bitmap++) {
		setCombination(fileName, bitmap);
		if(exists(path))
			return false;
	}
	return true;
}

bool isPassCombination(char* word, int bitmap) {
	for(int i = 0; i < strlen(word); i++) {
		if(!isalpha(word[i]) && bitmap % 2 == 1)
			return true;
		bitmap = bitmap / 2;
	}
	return false;
}

bool setCombination(char* word, int bitmap) {
	if(isPassCombination(word, bitmap)) {
		errno = EPERM;
		return false;
	}

	for(int i = 0; i < strlen(word); i++) {
		if(isalpha(word[i]))
			word[i] = (bitmap % 2 == 1) ? toupper(word[i]) : tolower(word[i]);
		bitmap = bitmap / 2;
	}
	return true;
}
