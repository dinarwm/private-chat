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

typedef struct node {
	int id;
	int socketfd;
	char name[MAX_NAME_LENGTH];
	struct node *next;
} node;

/* Global variables */
node *list;
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
  * @return node*|NULL
  */
node *find(int id) {

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
 node *new(int id, int socketfd, char *name) {
 	node *ans;

 	ans = (node *)malloc(sizeof(node));
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
void push(node *x) {

}

 /**
  * Remove node from the list by given id. If removing
  * is success, return 1. Otherwise, return 0.
  *
  * @param int id
  * @return int 1|0
  */
int pop(int id) {

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
  * Client maint thread.
  */
void *client_thread(void *arg) {
	node *data;
	int id;
	int socketfd;
	char name[MAX_NAME_LENGTH];

	data = (node *)arg;
	id = data->id;
	socketfd = data->socketfd;
	strcpy(name, data->name);

	printf(" (%d) Entering thread. Socket = %d\n", id, socketfd);

	char buffer[MAX_BUFFER];
	int ln = 1;
	while (ln > 0) {
		bzero(buffer, MAX_BUFFER);
		ln = my_read(socketfd, buffer, MAX_BUFFER);
		printf(" (%d) Recv: \"%s\"\n", id, buffer);
		printf(" (%d) Len: %d\n", id, ln);
		my_write(socketfd, buffer, strlen(buffer)+1);
		printf(" (%d) Send: \"%s\"\n", id, buffer);
	}
	close(socketfd);
	printf(" (%d) Close client with socket descriptor %d\n", id, socketfd);
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
	int i;
	for (i = 1; isLoop; i++) {
		int clientsock = accept(servsock, (struct sockaddr*) NULL, NULL);
		printf(" (%d) Accept client with socket descriptor %d\n", i, clientsock);

		node *pi = new(i, clientsock, "Name");
		pthread_create(&threads[i], NULL, client_thread, (void *)pi);
	}

	printf("Server is closing.");

	return 0;
}
