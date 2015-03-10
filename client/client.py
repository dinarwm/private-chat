import socket
import sys
import threading

host = '10.151.43.223'
port = 22001
size = 1024
login = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

sys.stdout.write('You are connected to server, please login to continue...\n')

try:
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
    
    #bikin GUI list
    print 'sukses login'
except KeyboardInterrupt:
    s.close()
    sys.exit(0)
