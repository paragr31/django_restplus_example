import socket
from threading import Thread
import random
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
    
    def chunks(self, string):
        for i in xrange(0, len(string), BUFFER_SIZE):
            yield string[i:i+BUFFER_SIZE]
        
    def get_string(self,length):
        try:
            if type(length) == int and length > 0:
                print("Request Come From IP %s For Random String Of Length %s"%(self.ip,length))
                return ''.join(random.choice(string.lowercase) for x in range(length))
            else:
                print("Requested Parameter should be Integer and Should be greator than Zero.")
        except Exception as err:
            print("Exception occured %s"% err)
    
    def get_num(self,length):
        try:
            if type(length) == int and length > 0:
                print("Request Come From IP %s For Random Number Of Length %s"%(self.ip,length))
                return random.randint(1,length)
            else:
                print("Requested Parameter should be Integer and Should be greator than Zero.")
        except Exception as err:
            print("Exception occured %s"% err)
    
    
    def run(self):
        recieved_msg = ""
        while True:
            try:
                mesg = self.sock.recv(BUFFER_SIZE)
                recieved_msg += mesg
                if not mesg:
                    print("Recieved Message %s from the client"% recieved_msg)
                if recieved_msg:
                    recieved_msg = json.loads(recieved_msg)
                print("Message Type = ",type(recieved_msg))
            except Exception as err:
                print("Error occured",err)
            break
			
        while True:
            try:
                if recieved_msg and type(recieved_msg) == dict:
                    for key in recieved_msg.keys():
                        if key.lower() == 'string':
                            string = self.get_string(recieved_msg[key])
                            if string:
                                for chunk in self.chunks(string):
                                    print("Sending String %s "% chunk)
                                    self.sock.send(chunk)
                        elif key.lower() == 'int':
                            num = self.get_num(recieved_msg[key])
                            if num:
                                print("Sending number %s "% num)
                                self.sock.send(str(num))
                else:
                    print("Recieved message is not of type dict")
            except Exception as err:
                print("Error occured",err)
            break
        self.sock.close()

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
    


        
        
