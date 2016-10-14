/*************************************************************************
*
* Copyright © 2016 Hope Bay Technologies, Inc. All rights reserved.
*
* File Name: hcfs_sys.h
* Abstract: This c header file for hcfs system operations.
*
* Revision History
* 2016/5/27 Modified after first code review.
*
**************************************************************************/

#ifndef GW20_HCFSAPI_SYS_H_
#define GW20_HCFSAPI_SYS_H_

#include <inttypes.h>

#define PASSPHRASE "lets encrypt configuration"

int32_t set_hcfs_config(char *arg_buf, uint32_t arg_len);

int32_t get_hcfs_config(char *arg_buf, uint32_t arg_len, char **value);

int32_t reload_hcfs_config();

int32_t toggle_cloud_sync(char *arg_buf, uint32_t arg_len);

int32_t get_sync_status();

int32_t reset_xfer_usage();

#endif  /* GW20_HCFSAPI_SYS_H_ */
