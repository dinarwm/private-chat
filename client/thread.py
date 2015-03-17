import select
import socket
import sys
import threading
 
class Server:
    def __init__(self):
        self.host = '10.151.43.223'
        self.port = 22001
        self.size = 1024
        self.server = None
        self.threads = []
        login = 0
 
    def open_socket(self):        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(10)
        
    def run(self):
        self.open_socket()
        while login==0:
            # masukin username
            cname = raw_input("Username: ")
            s.send('login:'+cname)
            msg = s.recv(size)
            auth = msg.split(':')[1]
            if auth=='1':
                login = 1
            else:
                print msg.split(':')[2]
        # muncul GUI list
        input = [self.server, sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])
            for s in inputready:
                #kalo terima chat
                if s == self.server:
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                #kalo mau ngechat
                elif s == sys.stdin:
                    #username tujuan diklik,
                    #program client memasukkan username tujuan ke var destination
                    destination = sys.stdin.readline()
                    #GUI buka layar chat baru
                    #STUCK -______-
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
 
        # close all threads
        self.server.close()
        for c in self.threads:
            c.join()

#buat threadnya
#belum selesai
class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
 
    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            print 'recv: ', self.address, data
            if data:
                self.client.send(data)
            else:
                self.client.close()
                running = 0
 
if __name__ == "__main__":
    s = Server()
    s.run() 
