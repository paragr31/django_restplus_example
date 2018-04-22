import socket
from threading import Thread
import json

TCP_IP = '192.168.56.102'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class Client(Thread):
    
    def __init__(self,ip,port,args):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.args = args
        print("New Thread started for IP : %s PORT : %s ARGS : %s." %(self.ip, self.port, self.args))
    
    def run(self):
        if self.args is not None and type(self.args) == dict:
            try:
                self.sock.connect((self.ip, self.port))
                self.sock.send(json.dumps(self.args).encode())
                
                recieved_msg = ""
                while True:
                    try:
                        msg = self.sock.recv(BUFFER_SIZE)
                        if not msg:
                            break
                        recieved_msg += msg
                    except Exception as err:
                        print("Error occured while receiveing data",err)
                        break
                
                if recieved_msg:
                    print("Got Responce as %s"% recieved_msg)
                else:
                    print("no responce recieved")
                self.sock.close()
            except Exception as err:
                print("Error Occured While Sending data %s"% err)
        else:
            print("Argument Should be defined and dict type.")
        return

        

abc = [{'string': 120},{'int': 10000}]

threads = []

for item in abc:
    newthread = Client(TCP_IP,TCP_PORT,item)
    newthread.start()
    threads.append(newthread)
    
for t in threads:
    t.join()

