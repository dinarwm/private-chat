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
```

### node_t *new_node(int id, int socketfd, char *name);

Buat `node_t` baru, atribut2nya dimasukkan ke parameter.
```c++
node_t *new_node(int id, int socketfd, char *name) {
	node_t *ans;

	ans = (node_t *)malloc(sizeof(node_t));
	ans->id = id;
	ans->socketfd = socketfd;
	strcpy(ans->name, name);
	ans->next = NULL;

	return ans;
}
```

### void push(node_t *node);

Masukkan `node_t` ke dalam `list`.
```c++
void push(node_t *node) {
	if (list == NULL) {
		list = x;
	} else {
		node->next = list;
		list = node;
	}
}
```

### int pop(int id);

Hapus `node` dengan `id` tertentu dari `list`.
```c++
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
```

## Socket dan Komunikasi dan Blablabla

### void handle_accept(int id, int clientsock);

Ini yang dilakuin kalau pertama ada client masuk.
```c++
void handle_accept(int id, int clientsock) {
	// harusnya disini diminta namanya dulu, baru nama nya disimpan.
	node_t *node = new_node(id, clientsock, "undefined");
	pthread_create(&threads[id], NULL, client_thread, (void *)node);
}
```

### Overriding function

Ini aku ngoverride fungsi `read` sama `write` biar manipulasinya
lebih gampang.
```c++
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
```

## Main Thread

Setiap ada client, langsung dibikinin `thread` baru, trus jalanin
fungsi ini.
```c++
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

	// harusnya disini dimintain nama client nya

	char buffer[MAX_BUFFER];
	int ln = 1;
	while (ln > 0) {
		bzero(buffer, MAX_BUFFER);
		ln = my_read(socketfd, buffer, MAX_BUFFER);
		printf(" (%d) Recv: \"%s\"\n", id, buffer);

		// harusnya disini ada handle protocol.

		my_write(socketfd, buffer, strlen(buffer)+1);
		printf(" (%d) Send: \"%s\"\n", id, buffer);
	}
	pop(id);
	close(socketfd);
	printf(" (%d) Close client with socket descriptor %d\n", id, socketfd);

	return NULL;
}
```

## To do
- Masalah login. Username validation, blablabla.
- Bikin fungsi `handle_protocol`, dipanggil dari `client_thread`.
- Broadcast list user jika ada client baru masuk.