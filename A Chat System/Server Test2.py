import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
FORMAT = "utf8"
DISCONNECT_MESSAGE = "!poof"
HEADER = 64
PORT = 5050
responsive = True
ADDR = (HOST, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
CHATLOG = []

def handle_client(conn, addr):
    global CHATLOG
    print(f"New Connection Obtained at {addr}")
    previousmsg = ""
    count = 0
    connected = True
    totalsentmessages = 0
    usernameflip = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if usernameflip:
                usernameflip = False
                username = msg
                print(f"User's name is {username}")
            else:
                if previousmsg != msg:
                    currentmsg = f" {username} {msg} "
                    CHATLOG.append(currentmsg)
                    print(currentmsg)
                    print(CHATLOG)
                    previousmsg = msg
            if msg == DISCONNECT_MESSAGE:
                print(f"user at {addr} has disconnected")
                connected = False
            if count == 0:
                pass
            else:
                currentchatlog = CHATLOG[totalsentmessages:]
                totalsentmessages = len(currentchatlog)
                sendchat = str(currentchatlog).encode(FORMAT)
                clientmsgsendout(conn, sendchat)
            count += 1
    
def clientmsgsendout(conn, msg):                             #
    msg_length = len(msg)                                    #
    send_length = str(msg_length).encode(FORMAT)             #
    send_length += b' ' * (HEADER - len(send_length))        #
    conn.send(send_length)                                   #
    conn.send(msg) 

def chatlogchecker():
    global CHATLOG
    while serveralive:
        if len(CHATLOG) > 25:
            CHATLOG = CHATLOG[1:]

def start():
    global CHATLOG
    server.listen()
    chatlogcheck = threading.Thread(target=chatlogchecker)
    chatlogcheck.start()
    while serveralive:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(threading.active_count() - 2)
        
        
        
print("[SERVER] Has Started")
print(f"[SERVER] Is Listening at {HOST}")

serveralive = True
start()
