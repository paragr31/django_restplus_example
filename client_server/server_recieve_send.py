import socket
from threading import Thread
from random import choice
import string
import json


TCP_IP = ''
TCP_PORT = 9001
BUFFER_SIZE = 1024


class ClientThread(Thread):
    
    
    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print("New Thread started for IP : %s PORT : %s" %(self.ip, self.port))
    
    
    def get_string(self,length):
        try:
            if type(length) == 'int' and length > 0:
                print("Request Come From IP %s For Random String Of Length %s"%(self.ip,length))
                return ''.join(random.choice(string.lowercase) for x in range(length))
            else:
                print("Requested Parameter should be Integer and Should be greator than Zero.")
        except Exception as err:
            print("Exception occured %s"% err)
    
    def get_num(self,length):
        try:
            if type(length) == 'int' and length > 0:
                print("Request Come From IP %s For Random Number Of Length %s"%(self.ip,length))
                return random.randint(1,length)
            else:
                print("Requested Parameter should be Integer and Should be greator than Zero.")
        except Exception as err:
            print("Exception occured %s"% err)
    
    
    def run(self):
        recieved_msg = ""
        while True:
            mesg = self.sock.recv(BUFFER_SIZE)
            recieved_msg += mesg
            if not mesg:
                print("Recieved Message %s from the client"% recieved_msg)
                break
        
        while True:
            pass
            break
                    
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))

threads = []

while True:
    tcpsock.listen(5)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print "Got connection from ", (ip, port)
    newthread = ClientThread(ip, port, conn)
    newthread.start()
    threads.append(newthread)
    
for t in threads:
    t.join()
    


        
        