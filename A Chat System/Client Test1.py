import socket
import threading

SERVER = ""
FORMAT = "utf8"
DISCONNECT_MESSAGE = "!poof"
HEADER = 64
PORT = 5050
responsive = True
allmessages = []
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_msg(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def recvmsg():
    message = client.recv(2048).decode(FORMAT)
    print(message)
    

def usermsg():
    sendingmsg = input("Something to say - ")
    send_msg(sendingmsg)
    if sendingmsg == DISCONNECT_MESSAGE:
        client.close()
    

alive = True
while alive:
    clientsend = threading.Thread(usermsg())
    clientrecv = threading.Thread(recvmsg())
    clientsend.start()
    clientrecv.start()
    
