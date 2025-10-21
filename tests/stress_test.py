import threading, socket, random, time

HOST, PORT = "127.0.0.1", 9889

def client_task(cid):
    try:
        with socket.create_connection((HOST, PORT)) as s:
            for i in range(5):  # each client does 5 operations
                key = f"key{cid}_{i}"
                value = f"value_from_client{cid}_{i}".encode()

                # SET
                header = f"set {key} 0 0 {len(value)}\r\n".encode()
                s.sendall(header)
                s.sendall(value + b"\r\n")
                resp = s.recv(1024).decode().strip()
                print(f"Client{cid}: SET {key} -> {resp}")

                time.sleep(random.uniform(0.05, 0.2))

                # GET
                s.sendall(f"get {key}\r\n".encode())
                resp = s.recv(1024).decode().strip()
                print(f"Client{cid}: GET {key} -> {resp}")

                time.sleep(random.uniform(0.05, 0.2))
    except Exception as e:
        print(f"Client{cid}: ERROR -> {e}")

def main():
    num_clients = 10000  # try a number of concurrent clients
    threads = []

    start = time.time()

    for cid in range(num_clients):
        t = threading.Thread(target=client_task, args=(cid,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.time()
    print(f"Completed {num_clients} clients in {end - start:.2f} seconds")

if __name__ == "__main__":
    main()
