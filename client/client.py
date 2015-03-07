import socket
import sys
import shutil
import select

host = 'localhost'
port = 1212
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

sys.stdout.write('You are connected to server, please login to continue...\n')

try:
    while 1:
        # baca input dan mengirim ketika ada input enter
        line = sys.stdin.readline()
        if line == '\n':
            break
        if line == 'Connected':
            sname = raw_input("Enter Username: ")
        print "You: " + line
        s.send(line)

except KeyboardInterrupt:
    s.close()
    sys.exit(0)
        
