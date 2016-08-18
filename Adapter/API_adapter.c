#include <dlfcn.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SO_PATH "libHCFS_api.so"

#define STAT 0
#define PIN 1
#define STATUS 2
#define UNPIN 3
#define RELOAD 4
#define SETSYNCPOINT 5
#define SETNOTIFY 6

int32_t main(int32_t argc, char **argv)
{
  int32_t code;
  void* lib_handle;       /* handle of the opened library */
  char* json_res = NULL;
  /* first define a function pointer variable to hold the function's address */
  void (*HCFS_stat) (char ** json_res);
  void (*HCFS_pin_path) (char ** json_res, char *  pin_path, char  pin_type);
  void (*HCFS_pin_status) ( char ** json_res, char *  pathname);
  void (*HCFS_unpin_path) (char ** json_res, char *  pin_path);
  void (*HCFS_reload_config)	(	char **	json_res	);
  void (*HCFS_set_sync_point)	(	char **	json_res	);
  void (*HCFS_set_notify_server) (char ** json_res, char *  path);

  if (argc < 1) {
    fprintf(stderr, "Invalid number of arguments: %s\n", *argv);
    exit(1);
  }
  if (strcasecmp(argv[1], "stat") == 0)
    code = STAT;
  else if (strcasecmp(argv[1], "pin") == 0)
    code = PIN;
  else if (strcasecmp(argv[1], "status") == 0)
    code = STATUS;
  else if (strcasecmp(argv[1], "unpin") == 0)
    code = UNPIN;
  else if (strcasecmp(argv[1], "reload") == 0)
    code = RELOAD;
  else if (strcasecmp(argv[1], "setsync") == 0)
    code = SETSYNCPOINT;
  else if (strcasecmp(argv[1], "setnotify") == 0)
    code = SETNOTIFY;
  else {
    printf("{'result':-1, 'msg':'Invalid arguments'}");
    exit(1);
  }
  lib_handle = dlopen(SO_PATH, RTLD_NOW);
  if (!lib_handle) {
    fprintf(stderr, "Error during dlopen(): %s\n", dlerror());
    exit(1);
  }
  
  /* then define a pointer to a possible error string */
  const char* error_msg;
  /* now locate the function in the library */
  HCFS_stat = dlsym(lib_handle, "HCFS_stat");
  HCFS_pin_path = dlsym(lib_handle, "HCFS_pin_path");
  HCFS_pin_status = dlsym(lib_handle, "HCFS_pin_status");
  HCFS_unpin_path = dlsym(lib_handle, "HCFS_unpin_path");
  HCFS_reload_config = dlsym(lib_handle, "HCFS_reload_config");
  HCFS_set_sync_point = dlsym(lib_handle, "HCFS_set_sync_point");
  HCFS_set_notify_server = dlsym(lib_handle, "HCFS_set_notify_server");

  /* check that no error occured */
  error_msg = dlerror();
  if (error_msg) {
    fprintf(stderr, "Error locating function - %s\n", error_msg);
    exit(1);
  }
  if(code == STAT)
    (*HCFS_stat)(&json_res);
  else if(code == PIN)
    (*HCFS_pin_path)(&json_res, argv[2], (char) 1);
  else if(code == STATUS)
    (*HCFS_pin_status)(&json_res, argv[2]);
  else if(code == UNPIN)
    (*HCFS_unpin_path)(&json_res, argv[2]);
  else if(code == RELOAD)
    (*HCFS_reload_config)(&json_res);
  else if(code == SETSYNCPOINT)
    (*HCFS_set_sync_point)(&json_res);
  else if(code == SETNOTIFY)
    (*HCFS_set_notify_server)(&json_res, argv[2]);
  fprintf(stdout, "%s", json_res);
  error_msg = dlerror();
  if (error_msg)
    fprintf(stderr, "Error in calling function - %s\n", error_msg);
  dlclose(lib_handle);
  return 0;
}

