import socket, threading, os

DATA_FILE = "data.txt"
store = {}
flags_store = {}

# -------- Helper: read exactly n bytes --------
def recv_exact(conn, n):
    data = b""
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            break
        data += chunk
    return data

# -------- Load persisted data at startup --------
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        while True:
            header = f.readline()
            if not header:
                break
            parts = header.strip().split()
            if len(parts) < 3 or parts[0].upper() != b"SET":
                break
            _, key, size = parts[:3]
            size = int(size)
            value = f.read(size)
            f.read(2)  # skip \r\n
            store[key.decode()] = value
            flags_store[key.decode()] = 0  # default flag

lock = threading.Lock()

def save_entry(key, value, flags=0):
    with open(DATA_FILE, "ab") as f:
        f.write(f"SET {key} {len(value)}\n".encode())
        f.write(value + b"\n")
    flags_store[key] = flags

def handle_client(conn, addr):
    with conn:
        while True:
            # ---- Read header line until CRLF ----
            header = b""
            while not header.endswith(b"\r\n"):
                chunk = conn.recv(1)
                if not chunk:
                    return
                header += chunk

            parts = header.strip().split()
            if not parts:
                break

            cmd = parts[0].lower()

            # ---------------- SET ----------------
            if cmd == b"set":
                noreply = False
                flags, exptime = 0, 0

                # Simplified format: set key bytes
                if len(parts) == 3:
                    key = parts[1].decode()
                    size = int(parts[2])
                # Full memcached format: set key flags exptime bytes [noreply]
                elif len(parts) in (5, 6):
                    key = parts[1].decode()
                    flags = int(parts[2])
                    exptime = int(parts[3])  # ignored
                    size = int(parts[4])
                    if len(parts) == 6 and parts[5].lower() == b"noreply":
                        noreply = True
                else:
                    conn.sendall(b"ERROR\r\n")
                    continue

                # ---- Read the value separately ----
                value = recv_exact(conn, size)
                conn.recv(2)  # skip trailing \r\n

                with lock:
                    store[key] = value
                    save_entry(key, value, flags)

                if not noreply:
                    conn.sendall(b"STORED\r\n")

            # ---------------- GET ----------------
            elif cmd == b"get" and len(parts) == 2:
                key = parts[1].decode()
                with lock:
                    value = store.get(key)
                    flags = flags_store.get(key, 0)
                if value:
                    response = (
                        f"VALUE {key} {flags} {len(value)}\r\n".encode()
                        + value + b"\r\nEND\r\n"
                    )
                    conn.sendall(response)
                else:
                    conn.sendall(b"END\r\n")

            else:
                conn.sendall(b"ERROR\r\n")

def main():
    HOST, PORT = "0.0.0.0", 9889
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=handle_client, args=(conn, addr), daemon=True
            ).start()

if __name__ == "__main__":
    main()
