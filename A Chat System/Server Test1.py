import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
FORMAT = "utf8"
DISCONNECT_MESSAGE = "!poof"
HEADER = 64
PORT = 5050
responsive = True
allmessages = []
ADDR = (HOST, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"New Connection Obtained at {addr}")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"Message {msg}")
            if msg == DISCONNECT_MESSAGE:
                print(f"user at {addr} has disconnected")
                connected = False
            returnmsg = ("Boo").encode(FORMAT)
            conn.send(returnmsg)

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(threading.active_count() - 1)
        
print("[SERVER] Has Started")
print(f"[SERVER] Is Listening at {HOST}")

start()
