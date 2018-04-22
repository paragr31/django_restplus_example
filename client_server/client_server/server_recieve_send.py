#!C:/ProgramData/Anaconda2/python

import win32serviceutil
import win32service
import win32event
import servicemanager

import socket
from threading import Thread
from SocketServer import ThreadingMixIn 
import random
import string
import json
import time

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
        time.sleep(20)
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

    
class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "SocketAPIServer"
    _svc_display_name_ = " Test Service to run socketserver on port 9091."


    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                          servicemanager.PYS_SERVICE_STARTED,
                          (self._svc_name_,''))
        self.main()

    def main(self):
        # Your business logic or call to any class should be here
        # this time it creates a text.txt and writes Test Service in a daily manner
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

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)

        
        
