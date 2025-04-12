import socket          # For network communication
import threading       # For handling multiple clients simultaneously 
import pickle          # For serializing/deserializing Python objects

# Tracker server configuration
TRACKER_HOST = 'localhost'
TRACKER_PORT = 9000

# Main data structure to track which peers have which chunks of files
# Structure: {file_id -> {chunk_index: [list_of_peer_addresses]}}
file_chunk_map = {}

def handle_client(conn, addr):
    """
    Handles communication with a connected peer.
    
    Args:
        conn: Socket connection to the peer
        addr: Address of the connected peer
    """
    try:
        # Receive serialized data from the peer
        data = conn.recv(4096)
        message = pickle.loads(data)

        # Process 'register' message type - when a peer announces chunks it has
        if message['type'] == 'register':
            file_id = message['file_id']        # Unique identifier for the file
            chunks = message['chunks']          # List of chunk indices the peer has
            peer_address = message['peer_address']  # Address where peer can be contacted
            
            # Create entry for new file if not already tracked
            if file_id not in file_chunk_map:
                file_chunk_map[file_id] = {}
                
            # Add peer to the list of peers for each chunk it has
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
