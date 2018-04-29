import socket
import json
import configs.settings as config
import time

TCP_IP = config.TCP_CLIENT_IP
TCP_PORT = config.TCP_PORT
BUFFER_SIZE = config.BUFFER_SIZE
args = {'string': 10240}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
data = json.dumps(args)
sock.send(str(len(data)))
time.sleep(1)
sock.send(data)
recieved_msg = ""
try:
    msg = sock.recv(BUFFER_SIZE).strip()
    while msg:
        recieved_msg += msg
        msg = sock.recv(BUFFER_SIZE)
        if not msg:
            print "Breaking client now"
            break
except Exception as err:
    print("Error occured while receiveing data",err)
    if recieved_msg:
        print("Got Responce as %s"% recieved_msg)
    else:
        print("no responce recieved")
sock.close()
print "Message = %s"% recieved_msg

