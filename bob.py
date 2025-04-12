import socket
import pickle
import os

# Configuration for connecting to the tracker
TRACKER_HOST = 'localhost'
TRACKER_PORT = 9000

def reliable_recv(sock):
    """
    Reliably receives potentially large serialized data over a socket.
    
    This handles the case where data might be split across multiple TCP packets.
    
    Args:
        sock: Socket connection to receive data from
        
    Returns:
        Deserialized Python object received from the socket
    """
    buffer = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        buffer += part
        try:
            return pickle.loads(buffer)
        except (pickle.UnpicklingError, EOFError):
            # Not enough data yet, continue receiving
            continue

def get_chunk_map_from_tracker(file_id):
    """
    Queries the tracker to get information about which peers have which chunks.
    
    Args:
        file_id: Identifier of the file to retrieve (typically filename)
        
    Returns:
        Dictionary mapping chunk indices to lists of peer addresses
    """
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
    """
    Requests a specific chunk from a peer.
    
    Args:
        peer_addr: Tuple of (host, port) identifying the peer
        chunk_index: The index of the chunk to request
        
    Returns:
        The chunk data if successful, None otherwise
    """
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
    """
    Reconstructs the original file from downloaded chunks.
    
    Args:
        total_chunks: Total number of chunks to combine
        output_path: Path where the reconstructed file will be saved
    """
    with open(output_path, 'wb') as f:
        for i in range(total_chunks):
            with open(f'bob_chunks/chunk_{i}.dat', 'rb') as chunk_file:
                f.write(chunk_file.read())
    print(f"[Bob] File reconstructed as '{output_path}'")

def run_bob():
    """Main function to run Bob's file download process"""
    # Get filename to download from user
    file_id = input("Enter the filename to download (same as what Alice used): ").strip()
    
    # Get chunk map from tracker
    chunk_map = get_chunk_map_from_tracker(file_id)

    if not chunk_map:
        print("[Bob] No data found for that file.")
        return

    # Ensure directory for downloaded chunks exists
    os.makedirs('bob_chunks', exist_ok=True)
    print(f"[Bob] Chunk map from tracker: {chunk_map}")

    # Download each chunk from available peers
    for chunk_index, peer_list in chunk_map.items():
        for peer in peer_list:
            # Try each peer until successful download
            chunk_data = request_chunk_from_peer(tuple(peer), chunk_index)
            if chunk_data:
                # Save the downloaded chunk
                with open(f'bob_chunks/chunk_{chunk_index}.dat', 'wb') as f:
                    f.write(chunk_data)
                print(f"[Bob] Downloaded chunk {chunk_index} from {peer}")
                break
            else:
                print(f"[Bob] Failed to get chunk {chunk_index} from {peer}")

    # Reconstruct the complete file from chunks
    total_chunks = len(chunk_map)
    reconstruct_file(total_chunks, f"reconstructed_{file_id}")

if __name__ == "__main__":
    run_bob()
