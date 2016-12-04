#include <dlfcn.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SO_PATH "libHCFS_api.so"

void* get_lib() {
  void* lib_handle = dlopen(SO_PATH, RTLD_NOW);
  if (!lib_handle) {
    fprintf(stderr, "Error during dlopen(): %s\n", dlerror());
    exit(1);
  }
  return lib_handle;
}

void check_lib_err(char* msg) {
  const char* error_msg = dlerror();
  if (error_msg) {
    fprintf(stderr, "Error %s - %s\n", msg, error_msg);
    exit(1);
  }
}

int32_t main(int32_t argc, char **argv)
{
  void* lib_handle;       /* handle of the opened library */
  char* json_res = NULL;

  /* first define a function pointer variable to hold the function's address */
  void (*HCFS_dir_status) (char **json_res, char *pathname);
  void (*HCFS_file_status) (char **json_res, char *pathname);
  void (*HCFS_stat) (char **json_res);
  void (*HCFS_pin_path) (char **json_res, char *pin_path, char pin_type);
  void (*HCFS_pin_status) (char **json_res, char *pathname);
  void (*HCFS_unpin_path) (char **json_res, char *pin_path);
  void (*HCFS_reload_config) (char **json_res);
  void (*HCFS_set_sync_point) (char **json_res);
  void (*HCFS_set_notify_server) (char **json_res, char *path);
  void (*HCFS_clear_sync_point) (char **json_res);
  void (*HCFS_get_config) (char **json_res, char *key);
  void (*HCFS_set_config) (char **json_res, char *key, char *value);

  lib_handle = get_lib();
  
  /* now locate the function in the library */
  HCFS_dir_status = dlsym(lib_handle, "HCFS_dir_status");
  HCFS_file_status = dlsym(lib_handle, "HCFS_file_status");
  HCFS_stat = dlsym(lib_handle, "HCFS_stat");
  HCFS_pin_path = dlsym(lib_handle, "HCFS_pin_path");
  HCFS_pin_status = dlsym(lib_handle, "HCFS_pin_status");
  HCFS_unpin_path = dlsym(lib_handle, "HCFS_unpin_path");
  HCFS_reload_config = dlsym(lib_handle, "HCFS_reload_config");
  HCFS_set_sync_point = dlsym(lib_handle, "HCFS_set_sync_point");
  HCFS_set_notify_server = dlsym(lib_handle, "HCFS_set_notify_server");
  HCFS_clear_sync_point = dlsym(lib_handle, "HCFS_clear_sync_point");
  HCFS_get_config = dlsym(lib_handle, "HCFS_get_config");
  HCFS_set_config = dlsym(lib_handle, "HCFS_set_config");

  check_lib_err("locating function");

  // argument passed to API
  // API(NULL); -> Segmentation fault
  // char* a = NULL;
  // API(a); -> Segmentation fault
  if(argc == 2) {
    if (strcasecmp(argv[1], "stat") == 0)
      (*HCFS_stat)(&json_res);
    else if (strcasecmp(argv[1], "reload") == 0)
      (*HCFS_reload_config)(&json_res);
    else if (strcasecmp(argv[1], "setsync") == 0)
      (*HCFS_set_sync_point)(&json_res);
    else if (strcasecmp(argv[1], "clearsync") == 0)
      (*HCFS_clear_sync_point)(&json_res);
  } else if(argc == 3) {
    if (strcasecmp(argv[1], "dirstatus") == 0)
      (*HCFS_dir_status)(&json_res, argv[2]);
    else if (strcasecmp(argv[1], "filestatus") == 0)
      (*HCFS_file_status)(&json_res, argv[2]);
    else if (strcasecmp(argv[1], "status") == 0)
      (*HCFS_pin_status)(&json_res, argv[2]);
    else if (strcasecmp(argv[1], "unpin") == 0)
      (*HCFS_unpin_path)(&json_res, argv[2]);
    else if (strcasecmp(argv[1], "setnotify") == 0)
      (*HCFS_set_notify_server)(&json_res, argv[2]);
    else if (strcasecmp(argv[1], "getconfig") == 0)
      (*HCFS_get_config)(&json_res, argv[2]);
  } else if(argc == 4) {
    if (strcasecmp(argv[1], "pin") == 0)
      (*HCFS_pin_path)(&json_res, argv[2], (char) 1);
    else if (strcasecmp(argv[1], "setconfig") == 0)
      (*HCFS_set_config)(&json_res, argv[2], argv[3]);
  } else
    goto err;

  check_lib_err("after called function");

  fprintf(stdout, "%s", json_res);
  dlclose(lib_handle);
  return 0;

err:
  fprintf(stderr, "Invalid argument number\n");
  return 0;
}

