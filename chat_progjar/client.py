import socket
import select
import sys
import os

HOST = '127.0.0.1'
PORT = 2323
BUF_SIZE = 4096
pesan = ""

def clearscreen(sock):
	os.system('clear')

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to " + str(HOST) + " : " + str(PORT)
    client_socket.connect((HOST, PORT))
    while 1:
    	socket_list = [sys.stdin, client_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        for sock in read_sockets:
		if sock == client_socket:
	        	data = sock.recv(4096)
			if data.split("\n",1)[0] == "os.system('clear')":
				clearscreen(sock)
				data = data.split("\n",1)[1]
			try:
				pecah = data.split("\n")[1]
			except:
				pecah = data
			try :
				if data == "exit!" :
					socket_list.remove(sock)
					os._exit(1)
				elif pecah.split("#")[0] == "group" or pecah.split("#")[0] == "personal":
					pesan = pecah
					os.system('clear')
					print pesan
				elif data.split(" ",1)[1] == "invitechatprivacy" :
					client_socket.send("2")
					ajakan = "ajak " + data.split(" ")[0]
					client_socket.send(ajakan)
					os.system('clear')
				else :
					if data.split(" ",1)[1] == "leave chat" and pesan == "":
						pass
					elif data != "os.system('clear')":	
						print data
			except:
				pass
		else :
        		data = sys.stdin.readline().split("\n")[0]
			files = ""
			if data == "exitpersonal()":
				files = pesan + data
				pesan = ""
				os.system('clear')
			elif data == "leavegroup()":
				files = pesan + data
				pesan = ""
				os.system('clear')
			elif data.split(" ")[0] == "transferfile": 
				files = files + pesan.split("#")[0] + "#" + pesan.split("#")[1] + "#" + pesan.split("#")[2] + "#transferfile#" + data.split(" ")[1]
			else:
				files = pesan + data
			client_socket.send(files)