#!C:/ProgramData/Anaconda2/python
__author__ = 'parag rajabhoj'
import win32serviceutil
import win32service
import win32event
import servicemanager

import SocketServer
import configs.settings as config
from libs.log_mgr import MyLogger
from libs.utils import MyUtilities
import json
import socket
import threading
import traceback
import os


class MyTCPSocket(SocketServer.BaseRequestHandler):
    """
    The Request Handler Class For This Server.
    
    This is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def myreceive(self):
        cur_thread = threading.current_thread()
        received_msg = ""
        length = self.request.recv(config.BUFFER_SIZE).strip()
        length = int(length)
        bytes_recved = 0
        while bytes_recved < length:
            try:
                message = self.request.recv(min(length - bytes_recved,config.BUFFER_SIZE)).strip()
                received_msg += message
                bytes_recved += len(message)
            except Exception as err:
                print "Exception %s occurred."% err
                break
        return received_msg
       
    def mysend(self):
        # Start processing request as per message received.
        try:
            if self.received_msg and type(self.received_msg) == dict:
                for key in self.received_msg.keys():
                    if key.lower() == 'string':
                        string = self.utils.get_string(self.received_msg[key])
                        if string:
                            for chunks in self.utils.get_chunks(string):
                                self.logger.info("Sending chunks %s"% chunks)
                                self.request.send(chunks)
                    elif key.lower() == 'int':
                        num = self.utils.get_num(self.received_msg[key])
                        if num:
                            self.logger.info("Sending number %s "% num)
                            self.request.send(str(num))
            else:
                self.logger.info("Recieved message %s is not of type dict"% self.received_msg)
        except Exception as err:
            self.logger.debug("Error Occured %s"% err)
            
    def handle(self):
        # self.request is the TCP socket connection to the client
        obj = MyLogger()
        self.logger = obj.getLogHandler()
        self.utils = MyUtilities(config.BUFFER_SIZE)
        self.received_msg = ""
        self.logger.info("Starting receiving message.")
        self.received_msg = self.myreceive()
        if self.received_msg:
            self.received_msg = json.loads(self.received_msg)
            self.logger.debug("Received Message is %s" % self.received_msg)
            self.logger.info("Starting sending message as per request.")
            self.mysend()
        self.request.close()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "SocketAPIServer"
    _svc_display_name_ = "Service to run socketserver on port %s"% config.TCP_PORT

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        obj = MyLogger()
        self.logger = obj.getLogHandler()
        self.logger.info("Started Service %s on port %s"% (self._svc_name_,config.TCP_PORT))

    def SvcStop(self):
        self.logger.info("Stopping Service %s"% self._svc_name_)
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.server.shutdown()
        self.server.server_close()
        
    def SvcDoRun(self):
        self.logger.info("Starting Service %s"% self._svc_name_)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                          servicemanager.PYS_SERVICE_STARTED,
                          (self._svc_name_,''))
        try:
            self.main()
        except Exception as err:
            servicemanager.LogErrorMsg(traceback.format_exc())
            self.logger.debug("Error Occured while starting Service %s. Error %s"% (self._svc_name_,err))
            os.exit(-1)
    
    def main(self):
        # Your business logic or call to any class should be here
        # this time it creates a text.txt and writes Test Service in a daily manner
        # Create the server, binding to localhost on port 9999
        self.server = ThreadedTCPServer((config.TCP_SERVER_IP, config.TCP_PORT), MyTCPSocket)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.server_thread = threading.Thread(target=self.server.serve_forever())
        # server_thread.daemon = True
        self.server_thread.start()
        self.logger.info("Server loop running in thread:", self.server_thread.name)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
    