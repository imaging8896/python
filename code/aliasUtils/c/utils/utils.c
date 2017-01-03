#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <math.h>
#include <sys/stat.h>

#include "utils.h"

int getCaseCombinationNum(char* word) {
	return (int)pow(2, strlen(word));
}

int getAlphaCaseCombinationNum(char* word) {
	int combinationNum = 1;
	for(int i = 0; i < strlen(word); i++) {
		if(isalpha(word[i]))
			combinationNum *= 2;
	}
	return combinationNum;
}

bool isDigit(char* str) {
	for(int i = 0; i < strlen(str); i++) {
		if(!isdigit(str[i]))
			return false;
	}
	return true;
}

long getIno(const char* path) {
  struct stat statBuf;
  if(stat(path, &statBuf) == 0)
    return statBuf.st_ino;
  else
    return -1;
}

bool exists(const char* path) {
	return access(path, F_OK) == 0;
}
