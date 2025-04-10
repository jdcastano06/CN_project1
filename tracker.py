import socket
import threading
import pickle

TRACKER_HOST = 'localhost'
TRACKER_PORT = 9000

# file_id -> {chunk_index: [peer_address]}
file_chunk_map = {}

def handle_client(conn, addr):
    try:
        data = conn.recv(4096)
        message = pickle.loads(data)

        if message['type'] == 'register':
            file_id = message['file_id']
            chunks = message['chunks']
            peer_address = message['peer_address']
            if file_id not in file_chunk_map:
                file_chunk_map[file_id] = {}
            for idx in chunks:
                file_chunk_map[file_id].setdefault(idx, []).append(peer_address)
            conn.sendall(pickle.dumps({'status': 'ok'}))

        elif message['type'] == 'get_peers':
            file_id = message['file_id']
            peers = file_chunk_map.get(file_id, {})
            conn.sendall(pickle.dumps(peers))

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def start_tracker():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((TRACKER_HOST, TRACKER_PORT))
        s.listen()
        print(f"[TRACKER] Running on {TRACKER_HOST}:{TRACKER_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_tracker()
