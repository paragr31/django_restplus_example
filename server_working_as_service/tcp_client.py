import socket
from threading import Thread
import json
import configs.settings as config
import time

TCP_IP = config.TCP_CLIENT_IP
TCP_PORT = config.TCP_PORT
BUFFER_SIZE = config.BUFFER_SIZE

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
                data = json.dumps(self.args)
                self.sock.send(str(len(data)))
                time.sleep(0.01)
                self.sock.sendall(data)
                # self.sock.close()
                recieved_msg = ""
                try:
                    msg = self.sock.recv(BUFFER_SIZE).strip()
                    while msg:
                        recieved_msg += msg
                        msg = self.sock.recv(BUFFER_SIZE).strip()
                        if not msg:
                            print "Breaking client now"
                            break
                except Exception as err:
                    print("Error occured while receiveing data",err)
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

        

abc = [{'string': 100},{'int': 10034500}]

# abc = [{'string': 10000}]

threads = []

for item in abc:
    newthread = Client(TCP_IP,TCP_PORT,item)
    newthread.start()
    threads.append(newthread)
    
for t in threads:
    t.join()

