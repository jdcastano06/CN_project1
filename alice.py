import socket
import pickle
import os
from utils import split_file

TRACKER_HOST = 'localhost'
TRACKER_PORT = 9000

PEERS = [
    ('localhost', 9101),
    ('localhost', 9102)
]

def send_chunk_to_peer(peer_addr, chunk_index):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(peer_addr)
        with open(f'chunks/chunk_{chunk_index}.dat', 'rb') as f:
            chunk_data = f.read()

        message = {
            'chunk_index': chunk_index,
            'chunk_data': chunk_data
        }
        s.sendall(pickle.dumps(message))
        response = s.recv(1024)
        print(f"[Alice] Sent chunk {chunk_index} to {peer_addr}, got:", response.decode())

def register_with_tracker(file_id, chunk_map):
    for idx, peer in chunk_map.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((TRACKER_HOST, TRACKER_PORT))
                message = {
                    'type': 'register',
                    'file_id': file_id,
                    'chunks': [idx],
                    'peer_address': peer
                }
                s.sendall(pickle.dumps(message))
                _ = s.recv(1024)  # receive 'ok'
        except Exception as e:
            print(f"[ERROR] Failed to register chunk {idx} to tracker: {e}")


def run_alice():
    file_path = input("Enter path to file to share: ").strip()
    os.makedirs('chunks', exist_ok=True)

    total_chunks = split_file(file_path)
    file_id = os.path.basename(file_path)

    print(f"[Alice] File split into {total_chunks} chunks.")

    # Send chunks to peers and remember who got what
    chunk_map = {}
    for i in range(total_chunks):
        assigned_peer = PEERS[i % len(PEERS)]
        send_chunk_to_peer(assigned_peer, i)
        chunk_map[i] = assigned_peer

    # Register with tracker
    register_with_tracker(file_id, chunk_map)
    print(f"[Alice] Registration with tracker complete.")

if __name__ == "__main__":
    run_alice()
