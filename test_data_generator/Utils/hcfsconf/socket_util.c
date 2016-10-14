/*************************************************************************
*
* Copyright © 2016 Hope Bay Technologies, Inc. All rights reserved.
*
* File Name: socket_util.c
* Abstract: This c source file for socket helpers.
*
* Revision History
* 2016/5/27 Modified after first code review.
*
**************************************************************************/

#include "socket_util.h"

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/uio.h>
#include <inttypes.h>

#include "global.h"

/************************************************************************
 * *
 * * Function name: get_hcfs_socket_conn
 * *        Inputs:
 * *       Summary: helper function to connect to hcfs socket.
 * *
 * *  Return value: Socket fd if successful.
 * *		    Otherwise returns negation of error code.
 * *
 * *************************************************************************/
int32_t get_hcfs_socket_conn()
{

	int32_t fd, status;
	struct sockaddr_un addr;

	addr.sun_family = AF_UNIX;
	strcpy(addr.sun_path, SOCK_PATH);
	fd = socket(AF_UNIX, SOCK_STREAM, 0);
	status = connect(fd, &addr, sizeof(addr));
	if (status < 0)
		return -errno;

	return fd;
}

/************************************************************************
 * *
 * * Function name: reads
 * *        Inputs:
 * *       Summary: A wrapper function for socket recv.
 * *
 * *  Return value: 0 if successful. Otherwise returns negation of error code.
 * *
 * *************************************************************************/
int32_t reads(int32_t fd, void *_buf, int32_t count)
{

	char *buf = (char *) _buf;
	int32_t total = 0, r = 0;

	if (count < 0)
		return -EINVAL;

	while (total < count) {
		r = recv(fd, buf + total, count - total,
			 MSG_NOSIGNAL);
		if (r < 0) {
			if (errno == EINTR)
				continue;
			return -errno;
		}
		if (r == 0)
			return -EIO;
		total += r;
	}
	return 0;
}

/************************************************************************
 * *
 * * Function name: sends
 * *        Inputs:
 * *       Summary: A wrapper function for socket send.
 * *
 * *  Return value: 0 if successful. Otherwise returns negation of error code.
 * *
 * *************************************************************************/
int32_t sends(int32_t fd, const void *_buf, int32_t count)
{
	const char *buf = (const char *) _buf;
	int32_t total = 0, s = 0;

	if (count < 0)
		return -EINVAL;

	while (total < count) {
		s = send(fd, buf + total, count - total,
			 MSG_NOSIGNAL);
		if (s < 0) {
			if (errno == EINTR)
				continue;
			return -errno;
		}
		total += s;
	}
	return 0;
}
