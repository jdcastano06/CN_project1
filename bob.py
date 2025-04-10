import socket
import pickle
import os

TRACKER_HOST = 'localhost'
TRACKER_PORT = 9000

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

def get_chunk_map_from_tracker(file_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TRACKER_HOST, TRACKER_PORT))
        message = {
            'type': 'get_peers',
            'file_id': file_id
        }
        s.sendall(pickle.dumps(message))
        chunk_map = reliable_recv(s)
    return chunk_map

def request_chunk_from_peer(peer_addr, chunk_index):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(peer_addr)
            message = {
                'request_chunk': chunk_index
            }
            s.sendall(pickle.dumps(message))
            response = reliable_recv(s)
            return response.get('chunk_data')
        except Exception as e:
            print(f"[Bob] Failed to connect to peer {peer_addr} for chunk {chunk_index}: {e}")
            return None

def reconstruct_file(total_chunks, output_path):
    with open(output_path, 'wb') as f:
        for i in range(total_chunks):
            with open(f'bob_chunks/chunk_{i}.dat', 'rb') as chunk_file:
                f.write(chunk_file.read())
    print(f"[Bob] File reconstructed as '{output_path}'")

def run_bob():
    file_id = input("Enter the filename to download (same as what Alice used): ").strip()
    chunk_map = get_chunk_map_from_tracker(file_id)

    if not chunk_map:
        print("[Bob] No data found for that file.")
        return

    os.makedirs('bob_chunks', exist_ok=True)
    print(f"[Bob] Chunk map from tracker: {chunk_map}")

    for chunk_index, peer_list in chunk_map.items():
        for peer in peer_list:
            chunk_data = request_chunk_from_peer(tuple(peer), chunk_index)
            if chunk_data:
                with open(f'bob_chunks/chunk_{chunk_index}.dat', 'wb') as f:
                    f.write(chunk_data)
                print(f"[Bob] Downloaded chunk {chunk_index} from {peer}")
                break
            else:
                print(f"[Bob] Failed to get chunk {chunk_index} from {peer}")

    total_chunks = len(chunk_map)
    reconstruct_file(total_chunks, f"reconstructed_{file_id}")

if __name__ == "__main__":
    run_bob()
