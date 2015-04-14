# server.c

## Linked list

### Variabel
Variabel atributnya client langsung tak jadikan satu `struct `
linked list nya. Biar ga ribet.
```c++
typedef struct node_t {
	int id;
	int socketfd;
	char name[MAX_NAME_LENGTH];
	struct node_t *next;
} node_t;
```

### node_t *find(int id);
Cari `node_t` dengan `id` tertentu. Kalau ga dapet, return `NULL`.
Kalau dapet ya syukur lah, return `node_t` nya.
```c++
node_t *_find(node_t *node, int id);
```

### node_t *find_by_name(char *name);
Cari `node_t` dengan `name` tertentu. Kalau ga dapet, return `NULL`.
Kalau dapet ya syukur lah, return `node_t` nya.
```c++
node_t *_find_by_name(node_t *node, char *name);
```

### node_t *new_node(int id, int socketfd, char *name);
Buat `node_t` baru, atribut2nya dimasukkan ke parameter.
```c++
node_t *new_node(int id, int socketfd, char *name);
```

### int list_size();
Ngitung panjang list sekarang
```c++
int list_size();
```

### void push(node_t *node);
Masukkan `node_t` ke dalam `list`.
```c++
void push(node_t *node);
```

### int pop(int id);

Hapus `node` dengan `id` tertentu dari `list`.
```c++
int pop(int id);
```

## Socket dan Komunikasi dan Protokol

### void broadcast(char *msg);
Mengirim pesan ke smua yang ada di `list`.
```c++
void broadcast(char *msg);
```

### void users();
Mengirim isi `list` ke smua yg ada di `list`.
```c++
void users();
```

### node_t *login(node_t *client, char buffer[]) {
Login dengan kata kunci di dalam buffer. Kalau gagal, return `NULL`.
Kalau berhasil return `node_t` berisi `client`.
```c++
node_t *login(node_t *client, char buffer[]);
```

### void logout(node_t *client);
Logout. Close `socket`, broadcast kalau ada yang off, dan remove `client` from `list`.
```c++
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
```

### void deliver(node_t *sender, char *msg);
Nerusin pesan dari pengirim ke penerima. Kalau penerimanya valid,
yaudah diterusin. Kalau penerima ga valid, bilang ke pengirim kalau eror.
```c++
void deliver(node_t *sender, char *msg);
```

## Main Thread
Setiap ada client, langsung dibikinin `thread` baru, trus jalanin
fungsi ini.

```c++
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
```

## Main function
Fungsi ``main()``.

```c++
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
```

## To do
- Masalah login. masih bug
- Enkripsi dan dekripsi butuh protokol baru?
