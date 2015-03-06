/**
 * Chat server.
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <pthread.h>

#define PORT 22001
#define MAX_QUEUES 10

typedef struct client_data {
	char name[16];
	int socketfd;
} client_data;

int servsock;

int main(int argc, char const *argv[]) {
	struct sockaddr_in servaddr;

	servsock = socket(AF_INET, SOCK_STREAM, 0);
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
		printf(" (%d) Accept client with file descriptor %d\n", i, clientsock);

		char str[100];
		bzero(str, 100);
		read(clientsock, str, 100);
		printf(" (%d) Recv: \"%s\"\n", i, str);
		write(clientsock, str, strlen(str)+1);
		printf(" (%d) Send: \"%s\"\n", i, str);

		close(clientsock);
		printf(" (%d) Close client with file descriptor %d\n", i, clientsock);
	}

	return 0;
}
