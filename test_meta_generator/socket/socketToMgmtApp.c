#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#define SOCKET_ADDRESS "mgmt.api.sock"
#define SERVERREPLYOK 1

int get_server_conn() {
	int32_t fd, status, sock_len;
	struct sockaddr_un addr;

	memset(&addr, 0, sizeof(struct sockaddr_un));
	addr.sun_family = AF_UNIX;
	addr.sun_path[0] = 0;
	strcpy(&(addr.sun_path[1]), SOCKET_ADDRESS);
	fd = socket(AF_UNIX, SOCK_STREAM, 0);
	if (fd < 0)
		return -errno;
	sock_len = 1 + strlen(SOCKET_ADDRESS) + offsetof(struct sockaddr_un, sun_path);
	status = connect(fd, (const struct sockaddr *) &addr, sock_len);
	if (status < 0) {
		close(fd);
		return -errno;
	}
	return fd;
}

int send_event_to_server(int32_t fd, char *events_in_json)
{
	int32_t r_size;
	int32_t ret_val = 0;
	char event_msg[strlen(events_in_json) + 2];

	/*
	 * Android API BufferedReader.readline() hangs until
	 * end-of-line is reached. So we put '\n' at the end
	 * of events_in_json string.
	 */
	sprintf(event_msg, "%s\n", events_in_json);

	r_size = send(fd, event_msg,
			strlen(event_msg), MSG_NOSIGNAL);
	if (r_size <= 0)
		return -errno;

	r_size = recv(fd, &ret_val, sizeof(int32_t), MSG_NOSIGNAL);
	if (ret_val == SERVERREPLYOK)
		return 0;
	else
		return -EINVAL;
}

int main(int argc, char **argv)
{
	int server_fd = get_server_conn();
	if (server_fd < 0) {
		fprintf(stderr, "Fail to get server socket error code:%d\n", server_fd);
		exit(1);
	}
	int ret_code = send_event_to_server(server_fd, "[{\"event_id\":1}]\n");
	if (ret_code < 0) {
		fprintf(stderr, "Fail to send event msg to server error code:%d\n", ret_code);
		exit(1);
	}
    return 0;
}

