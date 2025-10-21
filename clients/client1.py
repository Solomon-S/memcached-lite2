import socket, time, random

HOST, PORT = "127.0.0.1", 9889

with socket.create_connection((HOST, PORT)) as s:

    #Key 1
    value1 = b"solomon_siang"
    cmd = f"set user1 0 0 {len(value1)}\r\n".encode() + value1 + b"\r\n"
    s.sendall(cmd)
    print("SET response:", s.recv(1024).decode())
    time.sleep(random.uniform(0.2, 1.0))

    #Key 2
    value2 = b"11/21/03"
    cmd = f"set bday1 0 0 {len(value2)}\r\n".encode() + value2 + b"\r\n"
    s.sendall(cmd)
    print("SET response:", s.recv(1024).decode())
    time.sleep(random.uniform(0.2, 1.0))

