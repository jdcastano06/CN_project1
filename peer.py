import socket
import threading
import pickle
import os

def reliable_recv(sock):
    buffer = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        buffer += part
        try:
            return pickle.loads(buffer)
        except (pickle.UnpicklingError, EOFError):
            continue

def handle_client(conn, addr, storage_dir):
    try:
        message = reliable_recv(conn)

        if 'chunk_data' in message:  # Alice sending a chunk
            chunk_index = message['chunk_index']
            chunk_data = message['chunk_data']

            with open(f"{storage_dir}/chunk_{chunk_index}.dat", 'wb') as f:
                f.write(chunk_data)

            print(f"[Peer] Stored chunk_{chunk_index}.dat from {addr}")
            conn.sendall(b"OK: chunk received")

        elif 'request_chunk' in message:  # Bob requesting a chunk
            chunk_index = message['request_chunk']
            file_path = f"{storage_dir}/chunk_{chunk_index}.dat"

            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    chunk_data = f.read()
                conn.sendall(pickle.dumps({'chunk_data': chunk_data}))
                print(f"[Peer] Sent chunk_{chunk_index}.dat to {addr}")
            else:
                conn.sendall(pickle.dumps({'error': 'Chunk not found'}))
                print(f"[Peer] Chunk {chunk_index} not found for {addr}")

    except Exception as e:
        print(f"[Peer] Error: {e}")
    finally:
        conn.close()

def run_peer(peer_port):
    peer_host = 'localhost'
    storage_dir = f'peer_{peer_port}_storage'
    os.makedirs(storage_dir, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((peer_host, peer_port))
        s.listen()
        print(f"[Peer] Listening on {peer_host}:{peer_port}, storing in {storage_dir}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, storage_dir)).start()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9101
    run_peer(port)
