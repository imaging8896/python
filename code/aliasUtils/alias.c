#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <libgen.h>
#include <ctype.h>
#include <math.h>
#include <errno.h>

void not_exist(const char* path) {
  if (access(path, F_OK) != -1) {
    fprintf(stdout, "%s:exists", path);
    exit(EXIT_FAILURE);
  }
}

void gen_alias(const char* path) {
  struct stat statBuf;
  int statRet;
  statRet = stat(path, &statBuf);
  if(statRet != 0) {
    fprintf(stdout, "%s:%s", path, strerror(errno));
    exit(EXIT_FAILURE);
  }
}

void get_ino(const char* path) {
  struct stat statBuf;
  int statRet;
  statRet = stat(path, &statBuf);
  if(statRet == 0)
    fprintf(stdout, "%ld\n", statBuf.st_ino);
  else {
    fprintf(stdout, "%s:%s", path, strerror(errno));
    exit(EXIT_FAILURE);
  }
}

void for_each_case_file_name_do(char* path, int max, void (*func)(const char* path)) {
  char* fileName = strstr(path, basename(path));
  int i;
  int j;
  int bit;
  int bitmap;
  int combination = (int)pow(2, strlen(fileName));
  int aliasNum = combination;
  if(max != -1 && max < combination)
     aliasNum = max;
  int isPassCombination = 1;
  for(i = 0; i < aliasNum; i++) {
     bitmap = i;
     for(j = 0; j < strlen(fileName); j++) {
	    bit = bitmap % 2;
        if(isalpha(fileName[j])) {
          if(bit == 1)
            fileName[j] = toupper(fileName[j]);
          else
            fileName[j] = tolower(fileName[j]);
        } else {
          if(bit == 1) {
            isPassCombination = 0;
            break;
          }
        }
		bitmap = bitmap / 2;
     }

     if(isPassCombination == 1)
       func(path);
     isPassCombination = 1;
  }
}

int32_t main(int32_t argc, char **argv)
{
  if (argc < 3) {
    fprintf(stderr, "Invalid number of arguments: %s\n", *argv);
    exit(1);
  }
  char* path = argv[2];
  int max = atoi(argv[3]);
  if(max <= 0)
    max = -1;
  
  if (strcasecmp(argv[1], "getinos") == 0)
    for_each_case_file_name_do(path, max, get_ino);
  else if (strcasecmp(argv[1], "genaliases") == 0)
    for_each_case_file_name_do(path, max, gen_alias);
  else if (strcasecmp(argv[1], "notexist") == 0)
    for_each_case_file_name_do(path, max, not_exist);
  else
    fprintf(stderr, "Invalid arguments: %s\n", *argv);
  return 0;
}

