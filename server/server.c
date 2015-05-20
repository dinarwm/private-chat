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
#define MAX_NAME_LENGTH 10
#define MAX_BUFFER 2048
#define LOGOUT_BUFFER 16
#define USERS_BUFFER 1024

typedef struct node_t {
	int id;
	int socketfd;
	char name[MAX_NAME_LENGTH + 1];
	struct node_t *next;
} node_t;

/* Global variables */
node_t *list;
pthread_t threads[MAX_THREADS];
/* End of global variables */

/**
 * Get node from the list by given id. If it 
 * doesn't exist, return NULL.
 *
 * @param int id
 *
 * @return node*|NULL
 */
node_t *_find(node_t *node, int id) {
	if (node == NULL) {
		return NULL;
	}
	if (node->id == id) {
		return node;
	}
	return _find(node->next, id);
}

node_t *find(int id) {
	return _find(list, id);
}

/**
 * Get node from the list by given name. If it 
 * doesn't exist, return NULL.
 *
 * @param char *name
 *
 * @return node*|NULL
 */

node_t *_find_by_name(node_t *node, char *name) {
	if (node == NULL) {
		return NULL;
	}
	if (!strcmp(node->name, name)) {
		return node;
	}
	return _find_by_name(node->next, name);
}

node_t *find_by_name(char *name) {
	return _find_by_name(list, name);
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
 * Print and return list size.
 *
 * @return int size
 */
int list_size() {
	node_t *temp = list;
	int i;
	for (i=0; temp != NULL; i++) {
		temp = temp->next;
	}
	printf("Current list size is %d.\n", i);
	return i;
}

/**
 * Add given node to the list.
 *
 * @param node*
 */
void push(node_t *node) {
	if (list == NULL) {
		list = node;
	} else {
		node->next = list;
		list = node;
	}
	list_size();
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
	if (list == NULL) return 0;

	node_t *temp = list;
	if (list->id == id) {
		list = list->next;
		free(temp);
		list_size();
		return 1;
	}
	while (temp->next != NULL) {
		if (temp->next->id == id) {
			temp->next = temp->next->next;
			free(temp->next);
			list_size();
			return 1;
		}
		temp = temp->next;
	}
	list_size();
	return 0;
}

/**
 * Broadcast msg to all client.
 *
 * @param char *msg
 */
void broadcast(char *msg) {
	node_t *temp = list;
	while (temp != NULL) {
		write(temp->socketfd, msg, strlen(msg) + 1);
		temp = temp->next;
	}
}

/**
 * Create a userlist in a string format:
 *   userlist:<id>#<name>:<id>#<name>\r\n
 * Then broadcast to all connected client.
 */
void users() {
	char ans[USERS_BUFFER];
	sprintf(ans, "users");
	node_t *temp = list;
	while (temp != NULL) {
		sprintf(ans, "%s:%d#%s", ans, temp->id, temp->name);
		temp = temp->next;
	}
	sprintf(ans, "%s\r\n", ans);
	broadcast(ans);

	return;
}

/**
 * Do login. If success, then assign username to the client
 * node and return the client node. Otherwise return NULL.
 *
 * @param node_t client.
 *
 * @return node_t|NULL client.
 */
node_t *login(node_t *client, char buffer[]) {
	int socketfd = client->socketfd;
	char *ptr;

	if (strlen(buffer) < 6) {
		printf(" (%d) Error login.\n", client->id);
		return NULL;
	}

	ptr = strtok(buffer, ":\r\n");

	if (strcmp(ptr, "login")) {
		printf(" (%d) Wrong login format: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Wrong login format.\r\n");
		write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	}

	ptr = strtok(NULL, ":\r\n");
	printf(" (%d) Name: %s\n", client->id, ptr);

	if (strchr(ptr, ':') || strchr(ptr, '#')) {
		printf(" (%d) Name contains forbidden character: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name invalid.\r\n");
		write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	} else if (strlen(ptr) > MAX_NAME_LENGTH) {
		printf(" (%d) Name is too long: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name length more than %d.\r\n", MAX_NAME_LENGTH);
		write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	} else if (strlen(ptr) < 4) {
		printf(" (%d) Name is too short: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name length less than 4.\r\n");
		write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	} else if (find_by_name(ptr) != NULL) {
		printf(" (%d) Name alredy used: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name alredy used.\r\n");
		write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	}

	strcpy(client->name, ptr);
	sprintf(buffer, "auth:1:Login success.\r\n");
	write(socketfd, buffer, strlen(buffer)+1);

	return client;
}

/**
 * Do logout. Close the socket descriptor. Broadcast to all
 * online users if someone is logout. Broadcast to all online
 * users the new online userlist. Finally pop the node_t.
 *
 * @param node_t *client.
 */
void logout(node_t *client) {
	int id = client->id;
	char buffer[LOGOUT_BUFFER];

	close(client->socketfd);
	printf(" (%d) Close client with socket descriptor %d.\n", id, client->socketfd);

	int pop_return = pop(client->id);
	printf(" (%d) Pop returns %d.\n", id, pop_return);

	sprintf(buffer, "off:%d\r\n", id);
	broadcast(buffer);
	users();
}

/**
 * Deliver the message to the recipient. Recipient id
 * is attached in the message. First, convert the message
 *   from : <recipient_id>:<message>\r\n
 *   to   : rcv:<sender_id>:<message>\r\n
 * but if the recipient isn't on the list, send to sender
 *   off:<recipient_id>\r\n
 *
 * @param node_t *sender node
 * @param char *msg sent to server
 */
void deliver(node_t *sender, char *msg) {
	char *temp;
	char *temptr;
	char buffer[MAX_BUFFER];

	temp = (char*)malloc(sizeof(char) * (strlen(msg) + 25));
	temptr = temp;

	msg = strtok(NULL, ":\r\n");
	int recipient_id = atoi(msg);

	node_t *recipient = find(recipient_id);
	if (recipient == NULL) {
		printf(" (%d) User with %d is offline.\n", sender->id, recipient_id);
		sprintf(buffer, "off:%d\r\n", recipient_id);
		write(sender->socketfd, buffer, strlen(buffer) + 1);
	} else {
		msg = strtok(NULL, "\r\n");
		sprintf(temp, "rcv:%d:%s\r\n", sender->id, msg);
		printf(" (%d) Send: %s\n", sender->id, temptr);
		write(recipient->socketfd, temptr, strlen(temptr) + 1);
	}
}

/**
 * Client main thread.
 *
 * @param node_t *arg client data who started this thread.
 */
void *client_thread(void *arg) {
	node_t *data;
	int id;
	int socketfd;
	int ln;
	char name[MAX_NAME_LENGTH +1];
	char buffer[MAX_BUFFER];

	/* Get client data from main() */
	data = (node_t *)arg;
	id = data->id;
	socketfd = data->socketfd;
	printf(" (%d) Entering thread.\n", id);

	/* Login */
	while (1) {
		bzero(buffer, MAX_BUFFER);
		ln = read(socketfd, buffer, MAX_BUFFER);
		if (ln == 0) {
			printf(" (%d) Quit while login.\n", id);
			logout(data);
			return NULL;
		}
		/* Authorizing */
		if (login(data, buffer) != NULL) {
			break;
		}
	}

	/* Push this client to the linked list */
	printf(" (%d) Login success.\n", id);
	push(data);

	/* Broadcast new user list */
	users();

	/* Chatting loop */
	ln = 1;
	while (ln > 0) {
		/* Read message from client */
		bzero(buffer, MAX_BUFFER);
		ln = read(socketfd, buffer, MAX_BUFFER);
		if (ln <= 0) break;

		/* Remove the trailing newline */
		char *ptr;
		ptr = strtok(buffer, "\r\n");
		printf(" (%d) Recv: \"%s\"\n", id, ptr);

		/* Processing protocol */
		ptr = strtok(ptr, ":");
		if (!strcmp(ptr, "quit")) {
			break;
		} else if (!strcmp(ptr, "send")) {
			deliver(data, ptr);
		} else {
			sprintf(buffer, "error:Unknown command: '%s'.\r\n", ptr);
			write(socketfd, buffer, strlen(buffer)+1);
			printf(" (%d) Send: Unknown command\n", id);
		}
	}

	/* Logout and leave thread */ 
	logout(data);

	return NULL;
}

/**
 * Main program.
 */
int main(int argc, char const *argv[]) {
	struct sockaddr_in servaddr;
	int servsock;
	list = NULL;

	/* Create socket */
	servsock = socket(AF_INET, SOCK_STREAM, 0);
	printf("Server socket created.\n");

	/* Credit to pak Bas and Djuned */
	int opt = 1;
	setsockopt(servsock, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt));
	printf("Socket options: SO_REUSEADDR.\n");

	/* Setup server address and port */
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htons(INADDR_ANY);
	servaddr.sin_port = htons(PORT);
	printf("Server address created.\n");

	/* Binding socket */
	if (bind(servsock, (struct sockaddr *) &servaddr, sizeof(servaddr)) < 0) {
		printf("Binding failed.\n");
		exit(3);
	}
	printf("Binding success.\n");

	/* Enable listen */
	listen(servsock, MAX_QUEUES);
	printf("Listen to max %d queues.\n", MAX_QUEUES);

	/* Accepting clients */
	int isLoop = 1;
	int id;
	for (id = 1; isLoop; id++) {
		int clientsock = accept(servsock, (struct sockaddr*) NULL, NULL);
		printf(" (%d) Accept client with socket descriptor %d\n", id, clientsock);
		node_t *node = new_node(id, clientsock, "undefined");
		pthread_create(&threads[id], NULL, client_thread, (void *)node);
	}

	printf("Server is closing.");

	return 0;
}
