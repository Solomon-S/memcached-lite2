import socket, time,random

HOST, PORT = "127.0.0.1", 9889

with socket.create_connection((HOST, PORT)) as s:
    s.sendall(b"get user1\r\n")
    print("GET key1 response:", s.recv(1024).decode())
    time.sleep(random.uniform(0.2, 1.0))

    s.sendall(b"get bday1\r\n")
    print("GET key2 response:", s.recv(1024).decode())
    time.sleep(random.uniform(0.2, 1.0))
