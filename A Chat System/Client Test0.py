import socket

HOST = ""
PORT = 56420

responsive = True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while responsive:
        words = bytes(input("What would you like to say - "), "utf8")
        s.sendall(words)
        data = s.recv(1024)
        data = str(data)[2:-1]
        if data == "stop":
            print("Communication has ended")
            s.sendall(b"stop")
            responsive = False
        else:
            print(f"Received {data}")




