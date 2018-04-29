#!C:/ProgramData/Anaconda2/python
__author__ = 'parag rajabhoj'
import SocketServer
import configs.settings as config
from libs.log_mgr import MyLogger
from libs.utils import MyUtilities
import json
import socket
import threading


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

if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((config.TCP_SERVER_IP, config.TCP_PORT), MyTCPSocket)
    print dir(server)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server_thread = threading.Thread(target=server.serve_forever)
    print dir(server_thread)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    server.shutdown()