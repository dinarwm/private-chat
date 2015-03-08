/**
 * Chat server.
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <pthread.h>

#define PORT 22001
#define MAX_QUEUES 10
#define MAX_THREADS 256
#define MAX_NAME_LENGTH 16
#define MAX_BUFFER 100

typedef struct node_t {
	int id;
	int socketfd;
	char name[MAX_NAME_LENGTH];
	struct node_t *next;
} node_t;

/* Global variables */
node_t *list;
pthread_t threads[MAX_THREADS];
/* End of global variables */

/**
 * Initialize global variables.
 */
void initialize() {
	list = NULL;
}

/**
 * Get node from the list by given id. If it 
 * doesn't exist, return NULL.
 *
 * @param int id
 *
 * @return node*|NULL
 */
node_t *find(int id) {
	return _find(list, id);
}

node_t *_find(node_t *node, int id) {
	if (node == NULL) {
		return NULL;
	}
	if (node->id == id) {
		return node;
	}
	return _find(node->next, id);
}

/**
 * New node.
 *
 * @param int id
 * @param int socketfd
 * @param char* name
 *
 * @return node*
 */
node_t *new_node(int id, int socketfd, char *name) {
	node_t *ans;

	ans = (node_t *)malloc(sizeof(node_t));
	ans->id = id;
	ans->socketfd = socketfd;
	strcpy(ans->name, name);
	ans->next = NULL;

	return ans;
}

/**
 * Add given node to the list.
 *
 * @param node*
 */
void push(node_t *node) {
	if (list == NULL) {
		list = x;
	} else {
		node->next = list;
		list = node;
	}
}

/**
 * Remove node from the list by given id. If removing
 * is success, return 1. Otherwise, return 0.
 *
 * @param int id
 *
 * @return int 1|0
 */
int pop(int id) {
	temp = list;
	if (list->id == id) {
		list = list->next;
		free(temp);
		return 1;
	}
	while (temp->next != null) {
		if (temp->next->id == id) {
			temp->next = temp->next->next;
			free(temp->next);
			return 1;
		}
		temp = temp->next;
	}
	return 0;
}

/**
 * Soft override to write().
 *
 * @param int sockfd file descriptor of the sending socket.
 * @param void *buf message.
 * @param size_t len length of the message.
 *
 * @return ssize_t the number of characters sent.
 */
ssize_t my_write(int sockfd, void *buf, size_t len) {
	ssize_t ans;
	ans = write(sockfd, buf, len);
	return ans;
}

/**
 * Soft override to read().
 *
 * @param int fd file descriptor of the sender socket.
 * @param void *buf buffer that will filled with message.
 * @param size_t count max length of the message.
 *
 * @return ssize_t the number of bytes received.
 */
ssize_t my_read(int fd, void *buf, size_t count) {
	ssize_t ans;
	ans = read(fd, buf, count);
	return ans;
}

/**
 * Client main thread.
 *
 * @param node_t *arg client who started this thread.
 */
void *client_thread(void *arg) {
	node_t *data;
	int id;
	int socketfd;
	char name[MAX_NAME_LENGTH];

	data = (node_t *)arg;
	id = data->id;
	socketfd = data->socketfd;
	strcpy(name, data->name);

	printf(" (%d) Entering thread.\n", id, socketfd);

	char buffer[MAX_BUFFER];
	int ln = 1;
	while (ln > 0) {
		bzero(buffer, MAX_BUFFER);
		ln = my_read(socketfd, buffer, MAX_BUFFER);
		printf(" (%d) Recv: \"%s\"\n", id, buffer);

		my_write(socketfd, buffer, strlen(buffer)+1);
		printf(" (%d) Send: \"%s\"\n", id, buffer);
	}
	pop(id);
	close(socketfd);
	printf(" (%d) Close client with socket descriptor %d\n", id, socketfd);

	return NULL;
}

/**
 * Main program.
 */
int main(int argc, char const *argv[]) {
	close(4);
	struct sockaddr_in servaddr;

	int servsock = socket(AF_INET, SOCK_STREAM, 0);
	printf("Server socket created.\n");

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htons(INADDR_ANY);
	servaddr.sin_port = htons(PORT);
	printf("Server address created.\n");

	bind(servsock, (struct sockaddr *) &servaddr, sizeof(servaddr));
	printf("Binding success.\n");

	listen(servsock, MAX_QUEUES);
	printf("Listen to max %d queues.\n", MAX_QUEUES);

	int isLoop = 1;
	int id;
	for (id = 1; isLoop; id++) {
		int clientsock = accept(servsock, (struct sockaddr*) NULL, NULL);
		printf(" (%d) Accept client with socket descriptor %d\n", id, clientsock);

		node_t *pi = new_node(id, clientsock, "Name");
		push(pi);
		pthread_create(&threads[id], NULL, client_thread, (void *)pi);
	}

	printf("Server is closing.");

	return 0;
}
