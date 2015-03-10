import socket
import sys
import thread

host = '10.151.43.223'
port = 22001
size = 2048
login = 0
listuser = {}
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

    msg = s.recv(size)
    words = msg.split(':')
    a = 0
    for word in words:
        if a == 0:
            a=a+1
            pass
        else:
            iduser = word.split('#')[0]
            username = word.split('#')[1]
            listuser[iduser] = username

    for x in listuser:
        print x+' : '+listuser[x]
    
except KeyboardInterrupt:
    s.close()
    sys.exit(0)

