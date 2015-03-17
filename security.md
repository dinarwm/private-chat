## Sistem Keamanan

### Metode Pengamanan

Metode yang digunakan adalah *Diffie-Hellman*, *Blum Blum Shub*,  *Viginere*, dan *Playfair*.

### Penjelasan

Program yang dibuat harus benar-benar aman. Pesan yang dikirim oleh client ke client lainnya harus di*enkripsi* dengan key yang hanya diketahui setiap pasangan client tersebut. Bahkan server pun tidak boleh tahu bagaimana cara mendekripsi pesan. Oleh karena itu program ini akan menggunakan *Diffie-Hellman Key Exchange* sebagai metode mengrimkan kunci.

Intinya adalah setiap hubungan *clien-client* dan *client-server* akan mempunyai kunci masing-masing yang hanya diketahui masing-masing pasangan. Setiap client yang baru terhubung ke server dan berhasil login, akan berbagi kunci. Lalu client akan berbagi kunci dengan semua client yang terhubung.

Nilai yang dibentuk dari hasil *Diffie-Hellman Key Exchange* hanya berupa sebuah angka, maka kita harus membuat *pseudo-random* dari sebuah angka menjadi sebuah kunci yang acak. Oleh karena itu kita akan membuat kunci sesungguhnya dengan menggunakan metode *Blum Blum Shub*.

Kira-kira seperti ini distribusi kunci yang dihasilkan. Kolom dan baris menunjukkan hubungan komunikasi dan kunci apa yang digunakan.

 | **Server** | **Alice** | **Bob** | **Cecil** | **Damon**
--- | --- | --- | --- | --- | ---
**Server** | | *aliceserverkey* | *bobserverkey* | *cecilserverkey* | *damonserverkey*
**Alice** | *aliceserverkey* | | *bobalicekey* | *cecilalicekey* | *damonalicekey*
**Bob** | *bobserverkey* | *bobalicekey* | | *cecilbobkey* | *damonbobkey*
**Cecil** | *cecilserverkey* | *cecilalicekey* | *cecilbobkey* | | *damoncecilkey*
**Damon** | *damonserverkey* | *damonalicekey* | *damonbobkey* | *damoncecilkey* |

Pada saat pengiriman `pesan` dari *client1* ke *client2*, *client1* akan mengenkripsi `recipient` dengan kunci *server*. *Client1* juga akan mengenkripsi `pesan` dengan kunci *client2*. Lalu setelah *client1* mengirim `pesan` melalui *server*, *server* hanya bisa mendekripsi `recipient` saja tanpa bisa mendekripsi `pesan`. *Server* akan mengenkripsi `sender` dengen kunci *client2* dan mengirimkan ke *client2* bersamaan dengan `pesan`. Akhirnya *client2* akan mengenkripsi `sender` dengan kunci *server* dan mengenkripsi `pesan` dengan kunci *client1*.

### Sekenario

#### Inisialisasi
*Alice* dan *Bob* adalah client. Perantaranya adalah *Server*. Untuk melakukan kesepakatan kunci, kedua belah pihak harus memiliki `p` dan `g` yang sama, lalu kedua belah pihak saling mengirim angka `A` dan `B` hasil perhitungan dengan angka tertentu yang hanya diketahui oleh setiap pihak. Dari kombinasi keempat angka tersebut maka akan terbentuk sebuah angka kunci yang pasti hanya diketahui oleh kedua belah pihak karena angka tersebut adalah hasil perhitungan.

#### *Alice* dan *Server*
- *Alice* berhasil login ke *Server*.
- *Server* mengirim `p` dan `g` ke *Alice*.
- *Alice* mengirim `A` ke *Server*.
- *Server* mengirim `B` ke *Alice*.
- __*Alice* dan *Server* menyepakati kunci khusus dari hasil perhitungan__.
- Karena tidak ada yang online selain *Alice*, *Alice* selanjutnya tidak 
melakukan apa-apa.

#### *Bob* dan *Server*
- *Bob* berhasil login ke *Server*.
- *Server* mengirim `p` dan `g` ke *Bob*.
- *Bob* mengirim A ke *Server*.
- *Server* mengirim B ke *Bob*.
- __*Bob* dan *Server* menyepakati kunci khusus dari hasil perhitungan__.
- *Bob* menyuruh *Server* membroadcast `p` dan `g` (beda dengan yang awal) 
ke semua client yang online. Karena yang online hanya *Alice*, *Server* 
mengirim `p` dan `g` ke *Alice*. *Server* juga memberi tahu *Alice* kalau 
yang membuat `p` dan `g` adalah *Bob*.
- *Alice* mengirim nilai `A` ke *Bob* melalui *Server*.
- *Bob* mengirim nilai `B` ke *Alice* melalui *Server*.
- __*Alice* dan *Bob* menyepakati kunci khusus dari hasil perhitungan__.
