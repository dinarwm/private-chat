# Final Project Pemrograman Jaringan E - Hudan Studiawan
# Achmad Saiful         5112100029
# Bima Nisrina Madjid   5112100019
# Server

import socket
import select
import threading
import os

HOST = ''
PORT = 2323
BUF_SIZE = 4096

class WhatsUpServer(threading.Thread):
    def __init__(self, client, address):
	threading.Thread.__init__(self)
	self.conn = client
	self.addr = address
	self.name = ""
	self.password = ""

    def login(self):
	clients.append(self.conn)
	msg = "Enter your username : "
	self.conn.send(msg)
	username = self.conn.recv(BUF_SIZE).split("\n")[0]
	self.name = username
	cekpassword = "kosong"
	password = ""
	msg = "Set your password : "
	for avaliable in availables:
     		a = 0
    		for isi in avaliable:
    			a = a + 1
    			if a == 2 :
    				if isi == self.name:
    					msg = "Enter your password : "
    					cekpassword = "ada"
    			if a == 3 and cekpassword == "ada" :
    				password = isi
				cekpassword = "kosong"
	self.conn.send(msg)
	cek = ""
	pswd = self.conn.recv(BUF_SIZE).split("\n")[0]
	if cekpassword == "ada" :
		if password == pswd :
			online.append(self.name)
			msg = "Selamat Datang " + self.name
			self.conn.send(msg)
			cek = "1"
		else :
			msg = "Password Salah"
			self.conn.send(msg)
			cek = "0"
	else :
		self.password = pswd
		availables.append([self.conn,self.name,self.password])
		online.append(self.name)
		print str(self.addr) + " as "+ self.name
		msg = "Selamat Datang " + self.name
		self.conn.send(msg)
		cek = "1"
	return cek

    def showlistonline(self):
	listonline = "os.system('clear')\nonline : \n"
	for list in online:
		if list != self.name:
			listonline = listonline + "\t - " + list + "\n";
    	self.conn.send(listonline)

    def chatpersonal(self,pilihan):
	self.showlistonline()
	msg = "\t <= back\nChoose wisely / back : "
	self.conn.send(msg)
	addr = ""
	data = self.conn.recv(BUF_SIZE)
	print data
	if data == "back":
		pilihan = "back"
	else :
		cek = "0"
		if data.split(" ")[0] == "ajak":
			cek = "1"
			data = data.split(" ")[1] 
		for avaliable in availables:
			a = 0
	    		for isi in avaliable:
	    			a = a + 1
	    			if a == 1 :
	    				addr = isi
	    			if a == 2 :
	    				if isi == data:
	    					pilihan = pilihan+ str(addr) + "#chat#"
						if cek == "0":
							ajakan = self.name + " invitechatprivacy"
							addr.send(ajakan)
	    					break
		msg = "Chat anda dengan " + data + " terhubung\n"
		online.remove(self.name)
		self.conn.send(msg)
	return pilihan

    def pilihan(self):
	msg = "\nMenu : \n\t1. List Online.\n\t2. Chat Personal.\n\t3. Chat Group.\n\t4. Logoff\nPilih menu nomer : "
	self.conn.send(msg)

    def chat(self,con,pesan):
	for avaliable in availables:
		a = 0
    		for isi in avaliable:
    			a = a + 1
    			if a == 1 :
    				if str(isi) == con:
					isi.send(pesan)

    def keyword(self,data):
    	if data.split("#")[0] == "personal":
		try:
			if data.split("#")[3] == "chat":
				pesan = data.split("#")[1] + " : " + data.split("#")[4]
				self.chat(data.split("#")[2],pesan)
		except :
			pilihan = self.chatpersonal(data)
			if pilihan == "back":
				return pilihan
			else:			
				self.conn.send(pilihan)
	elif data.split("#")[0] == "group":
		try:
			if data.split("#")[3] == "chat":
				pesan = data.split("#")[1] + " : " + data.split("#")[4]
				listmember = []				
				for group in groups:				
					a = 0
					cek = 0
					for isi in group:
						if a == 0 and isi == data.split("#")[2]:	
							cek = 1
						if a == 1 and cek == 1 :
							listmember = isi
						a = a + 1
				for member in listmember:
					if member != self.conn:
						member.send(pesan)				
		except :
			pilihan = self.group(data)
			if pilihan == "back":
				return pilihan
			else:			
				self.conn.send(pilihan)

    def logoff(self):
	self.conn.send('exit!')
	online.remove(self.name)
	print self.name + " was offline"
	clients.remove(self.conn)
	exit()
	self.conn.close()

    def group(self,pilihan):
	msg = "\nMenu Grup: \n\t1. Create Group\n\t2. Join Group\nChoose wisely : "
	self.conn.send(msg)
	data = self.conn.recv(BUF_SIZE)
	if data == "1":
		msg = "Name Group : "
		self.conn.send(msg)
		data = self.conn.recv(BUF_SIZE)
		conn = []
		conn.append(self.conn)
		groups.append([data,conn])
		pilihan = pilihan + data + "#chat#"
		print pilihan
	elif data == "2":
		msg = "\nList Group: "
		for group in groups:
	    		for isi in group:
				msg = msg + "\n\t- " + isi
				break
		msg = msg + "\n\t <= back\nChoose wisely / back : "
		self.conn.send(msg)
		data = self.conn.recv(BUF_SIZE)
		if data == "back":
			pilihan = "back"
		else :
			simpan = ""
			listmember = []
			count = -1
			urutanke = 0
			for group in groups:
				a = -1
				count = count + 1
		    		for isi in group:
					a = a+1
					if a == 1 and isi == data:
						urutanke = count
					if a != 0:
						listmember = isi
			listmember.append(self.conn)
			del groups[urutanke]
			groups.append([data,listmember])
			kopi = []
			for group in groups:
				a = -1
				count = count + 1
		    		for isi in group:
					a = a+1
					if a == 1 and isi == data:
						urutanke = count
					if a != 0:
						kopi = isi
			pilihan = pilihan + data + "#chat#"
			online.remove(self.name)
	return pilihan
	
    def leavegroup(self,namagroup):
	simpan = ""
	listmember = []
	fixmember = []
	count = -1
	urutanke = 0
	for group in groups:
		a = -1
		count = count + 1
    		for isi in group:
			a = a+1
			if a == 1 and isi == namagroup:
				urutanke = count
			if a != 0:
				listmember = isi
	nmember = 0
	for list in listmember:
		if list != self.conn:
			list.send("==== " + self.name + " leave group ====")
			nmember = nmember + 1
			fixmember.append(list)
	if nmember == 0:
		del groups[urutanke]
	else : 
		del groups[urutanke]
		groups.append([namagroup,fixmember])

    def run(self):
	cek = self.login()
	if cek == "1":
		while 1:
			pilihan = ""
			self.pilihan()
			data = self.conn.recv(BUF_SIZE)
			if data == "1" :
				self.showlistonline()
			elif data == "2" :
	    			pilihan = "personal#" + self.name + "#"
			elif data == "3" :
	    			pilihan = "group#" + self.name + "#"
	    		elif data == "4" :
	    			self.logoff()
	    		choice = self.keyword(pilihan)
			while 1:
				for available in availables :
					print available
				if choice == "back":
					break
				if data == "1" :
					break
				data = self.conn.recv(BUF_SIZE)
				cekleavegroup = ""
				namagroup = ""
				try:
					cekleavegroup = data.split("#")[4]
					namagroup = data.split("#")[2]
				except:
					pass
				if cekleavegroup == "leavegroup()" :
					online.append(self.name)
					pilihan = ""
					self.leavegroup(namagroup)
					break	
				elif cekleavegroup == "exitpersonal()":
					online.append(self.name)
					pilihan = ""
					self.chat(namagroup,self.name + " leave chat")
					break
				else:
					self.keyword(data)
	else :
		self.logoff()

if __name__ == "__main__":
    global clients
    global availables
    global online
    global groups

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    clients = []
    availables = []
    online = []
    groups = []

    os.system('clear')
    print "====================================="
    print "Final Project Pemrograman Jaringan E"
    print "Achmad Saiful & Bima Nisrina Madjid"
    print "====================================="
    print "Chat server started on port " + str(PORT)

    clients.append(server_socket)
    while 1:
	read_sockets,write_sockets,error_sockets = select.select(clients,[],[])
	for sock in read_sockets:
	    if sock == server_socket:
		client,address = server_socket.accept()
		clients.append(client)
		print "Client (%s, %s) connected" % address
		server = WhatsUpServer(client,address)
		server.start()
	    else:
		pass
    server_socket.close()
