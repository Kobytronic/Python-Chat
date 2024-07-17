import socket
import threading

HOST = ""
PORT = 56420
responsive = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while responsive:
            data = conn.recv(1024)
            if not data:
                break
            data = str(data)[2:-1]
            if data == "stop":
                print("Communication has ended")
                conn.sendall(b"stop")
                conn.close()
                responsive = False
            else:
                print("recieved",data)
                words = input("What would you like to say - ")
                words = bytes(words, "utf8")
                conn.sendall(words)
