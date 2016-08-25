/*************************************************************************
*
* Copyright © 2016 Hope Bay Technologies, Inc. All rights reserved.
*
* File Name: global.h
* Abstract: This c header file for global settings for HCFS.
*
* Revision History
* 2016/5/27 Modified after first code review.
*
**************************************************************************/

#ifndef GW20_HCFSAPI_GLOBAL_H_
#define GW20_HCFSAPI_GLOBAL_H_

#define TRUE 1
#define FALSE 0

#define CONFIG_PATH "/data/hcfs.conf"
#define DB_PATH "/data/data/com.hopebaytech.hcfsmgmt/databases/uid.db"
#define SOCK_PATH "/dev/shm/hcfs_reporter"
#define API_SOCK_PATH "/data/data/com.hopebaytech.hcfsmgmt/hcfsapid_sock"

#define LOG_PATH "/data"
#define LOG_NAME "hcfsapid.log"
#define LOG_LEVEL 4

/* List of API codes */
#define TERMINATE 0
#define VOLSTAT 1
#define TESTAPI 2
#define ECHOTEST 3
#define CREATEFS 4
#define MOUNTFS 5
#define DELETEFS 6
#define CHECKFS 7
#define LISTFS 8
#define UNMOUNTFS 9
#define CHECKMOUNT 10
#define UNMOUNTALL 11
#define PIN 12
#define UNPIN 13
#define CHECKDIRSTAT 14
#define GETVOLSIZE 15
#define GETCLOUDSIZE 16
#define GETPINSIZE 17
#define GETCACHESIZE 18
#define CHECKLOC 19
#define CHECKPIN 20
#define GETMAXPINSIZE 21
#define GETMAXCACHESIZE 22
#define CLOUDSTAT 23
#define GETDIRTYCACHESIZE 24
#define GETXFERSTAT 25
#define RESETXFERSTAT 26
#define SETSYNCSWITCH 27
#define GETSYNCSWITCH 28
#define GETSYNCSTAT 29
#define RELOADCONFIG 30
#define GETQUOTA 31
#define TRIGGERUPDATEQUOTA 32
#define CHANGELOG 33
#define UNPINDIRTYSIZE 34
#define OCCUPIEDSIZE 35
#define GETXFERSTATUS 36

#define SETCONFIG 48
#define GETCONFIG 49
#define GETSTAT 50
#define SYSREBOOT 51
#define QUERYPKGUID 52

#endif  /* GW20_HCFSAPI_GLOBAL_H_ */
