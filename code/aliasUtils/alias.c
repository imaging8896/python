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

int32_t main(int32_t argc, char **argv)
{
  if (argc < 1) {
    fprintf(stderr, "Invalid number of arguments: %s\n", *argv);
    exit(1);
  }
  char* path = argv[1];
  char* fileName = basename(path);
  struct stat statBuf;
  
  int i;
  int j;
  int bit;
  int bitmap;
  int combination = (int)pow(2, strlen(fileName));
  int isPassCombination = 1;
  int statRet;
  for(i = 0; i < combination; i++) {
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

     if(isPassCombination == 1) {
	   statRet = stat(path, &statBuf);
       if(statRet == 0)
         fprintf(stdout, "%d\n", statBuf.st_ino);
       else {
         fprintf(stdout, "%s:%s", path, strerror(errno));
         return -1;
       }
     }
     isPassCombination = 1;
  }
  return 0;
}

