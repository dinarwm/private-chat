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
```

### node_t *find_by_name(char *name);
Cari `node_t` dengan `name` tertentu. Kalau ga dapet, return `NULL`.
Kalau dapet ya syukur lah, return `node_t` nya.
```c++
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

### int list_size();
Ngitung panjang list sekarang
```c++
int list_size() {
	node_t *temp = list;
	int i;
	for (i=0; temp != NULL; i++) {
		temp = temp->next;
	}
	printf("Current list size is %d.\n", i);
	return i;
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
	list_size();
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
		list_size();
		return 1;
	}
	while (temp->next != null) {
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
```

## Socket dan Komunikasi dan Protokol

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

### void broadcast(char *msg);
Mengirim pesan ke smua yang ada di `list`.
```c++
void broadcast(char *msg) {
	node_t *temp = list;
	while (temp != NULL) {
		my_write(temp->socketfd, msg, strlen(msg) + 1);
		temp = temp->next;
	}
}
```

### void users();
Mengirim isi `list` ke smua yg ada di `list`.
```c++
void users() {
	char ans[2048];
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
```

### node_t *login(node_t *client, char buffer[]) {
Login dengan kata kunci di dalam buffer. Kalau gagal, return `NULL`.
Kalau berhasil return `node_t` berisi `client`.
```c++
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
		my_write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	}

	ptr = strtok(NULL, ":\r\n");
	printf(" (%d) Name: %s\n", client->id, ptr);

	if (strchr(ptr, ':') || strchr(ptr, '#')) {
		printf(" (%d) Name contains forbidden character: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name invalid.\r\n");
		my_write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	} else if (strlen(ptr) > MAX_NAME_LENGTH) {
		printf(" (%d) Name is too long: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name length more than %d.\r\n", MAX_NAME_LENGTH);
		my_write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	} else if (strlen(ptr) < 4) {
		printf(" (%d) Name is too short: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name length less than 4.\r\n");
		my_write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	} else if (find_by_name(ptr) != NULL) {
		printf(" (%d) Name alredy used: '%s'.\n", client->id, ptr);
		sprintf(buffer, "auth:0:Name alredy used.\r\n");
		my_write(socketfd, buffer, strlen(buffer)+1);
		return NULL;
	}

	strcpy(client->name, ptr);
	sprintf(buffer, "auth:1:Login success.\r\n");
	my_write(socketfd, buffer, strlen(buffer)+1);

	return client;
}
```

### void logout(node_t *client);
Logout. Close `socket`, broadcast kalau ada yang off, dan remove `client` from `list`.
```c++
void logout(node_t *client) {
	char buffer[16];
	close(client->socketfd);
	printf(" (%d) Close client with socket descriptor %d.\n", client->id, client->socketfd);
	
	sprintf(buffer, "off:%d\r\n", client->id);
	broadcast(buffer);

	int id = client->id;
	int pop_return = pop(client->id);
	printf(" (%d) Pop returns %d.\n", id, pop_return);
}
```

### void deliver(node_t *sender, char *msg);
Nerusin pesan dari pengirim ke penerima. Kalau penerimanya valid,
yaudah diterusin. Kalau penerima ga valid, bilang ke pengirim kalau eror.
```c++
void deliver(node_t *sender, char *msg) {
	char temp[strlen(msg) + 25];
	char buffer[100];

	msg = strtok(NULL, ":\r\n");
	int recipient_id = atoi(msg);

	node_t *recipient = find(recipient_id);
	if (recipient == NULL) {
		printf(" (%d) User with %d is offline.\n", sender->id, recipient_id);
		sprintf(buffer, "off:%d\r\n", recipient_id);
		my_write(sender->socketfd, buffer, strlen(buffer) + 1);
	} else {
		msg = strtok(NULL, "\r\n");
		sprintf(temp, "rcv:%d:%s\r\n", sender->id, msg);
		printf(" (%d) Send: rcv:%d:%s\n", sender->id, sender->id, msg);
		my_write(recipient->socketfd, temp, strlen(temp) + 1);
	}
}
```

## Main Thread
Setiap ada client, langsung dibikinin `thread` baru, trus jalanin
fungsi ini.

### Definisi variabel
```c++
void *client_thread(void *arg) {
	node_t *data;
	int id;
	int socketfd;
	int ln;
	char name[MAX_NAME_LENGTH +1];
	char buffer[MAX_BUFFER];
```
### Inisialisasi data client
Biar gampang manggilnya
```c+++
	data = (node_t *)arg;
	id = data->id;
	socketfd = data->socketfd;
```
### Masuk ke alur program
#### Login
```c+++
	printf(" (%d) Entering thread.\n", id);
	while (1) {
		bzero(buffer, MAX_BUFFER);
		ln = my_read(socketfd, buffer, MAX_BUFFER);
		if (ln == 0) {
			printf(" (%d) Quit while login.\n", id);
			logout(data);
			return NULL;
		}
		if (login(data, buffer) != NULL) {
			break;
		}
	}

	printf(" (%d) Login success.\n", id);
	push(data);
	users();
```
#### Chatting
```c+++
	ln = 1;
	while (ln > 0) {
		bzero(buffer, MAX_BUFFER);
		ln = my_read(socketfd, buffer, MAX_BUFFER);
		if (ln <= 0) break;

		char *ptr;
		ptr = strtok(buffer, "\r\n");
		printf(" (%d) Recv: \"%s\"\n", id, ptr);

		ptr = strtok(ptr, ":");

		if (!strcmp(ptr, "quit")) {
			break;
		} else if (!strcmp(ptr, "send")) {
			deliver(data, ptr);
		} else {
			sprintf(buffer, "error:Unknown command: '%s'.\r\n", ptr);
			my_write(socketfd, buffer, strlen(buffer)+1);
			printf(" (%d) Send: Unknown command\n", id);
		}
	}
```
### Finally
Kalau udah keluar dari main loop. Client memutus koneksi.
```c++
	logout(data);

	return NULL;
}
```

## To do
- Masalah login. masih bug
- Bug kalau ada escape character dari client
- `\r\n` itu kepakai ga ya?
