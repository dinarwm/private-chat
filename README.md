## Private-chat

### Deskripsi
Program chat client-server, client hanya bisa chatting secara 
personal (bukan broadcast). Server dibuat dengan bahasa c, sedangkan
client dibuat dengan bahasa python.

### Protokol
Pengirim | Protokol | Deskripsi
--- | --- | ---
Client | `login:<username>` | Login dengan username
Server | `auth:<1|0>:<errmsg>` | Ngasih tau login gagal apa ga. Error msgnya apa.
Server | `users:<id>#<username>:<id>#<username>` | Ngasih list yg online.
Server | `off:<id>` | Ngasih tau kalau id itu lagi offline.
Client | `send:<id>:<msg>` | Ngirim pesan ke id.
Server | `rcv:<id>:<msg>` | Dapet pesan dari id.
Client | `(null)` atau `quit` | Logout

### Flowchart Login
No | Server | Client
--- | --- | ---
1 | | Mengirim koneksi ke server
2 | Menerima koneksi dari client | 
3 | | Login dengan `login:username`
4b | Jika login gagal, kirim `auth:0:errormsg` kembali ke 3 | 
4a | Jika login sukses, kirim `auth:1` | 
5 | Broadcast `users:<id>#<username>:..` yang login | 

### Contoh List User
id | name
--- | ---
1 | icang
2 | dinar
3 | dees
4 | ipul

### Flowchart Main Program
No | Server | Client
--- | --- | ---
1 |  | icang mengirim pesan ke dinar melalui server
 |  | `send:2:halo`
2a | Jika user tidak ada, kirim `off:2` | 
2b | Jika user ada, kirim ke dinar `rcv:1:halo` | 

### Flowchart Logout
No | Server | Client
--- | --- | ---
1 |  | Dinar logout, kirim `quit`
2 | Broadcast kalau dinar logout: `off:2` | 
3 | Broadcast userlist baru `users:<id>#<username>:..` | 
