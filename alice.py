import socket
import pickle
import os
from utils import split_file

# Configuration for connecting to the tracker server
TRACKER_HOST = 'localhost'
TRACKER_PORT = 9000

# List of available peers where file chunks will be stored
# Each peer is identified by (host, port) tuple
PEERS = [
    ('localhost', 9101),
    ('localhost', 9102)
]

def send_chunk_to_peer(peer_addr, chunk_index):
    """
    Sends a specific chunk to a designated peer.
    
    Args:
        peer_addr: Tuple of (host, port) identifying the peer
        chunk_index: The index number of the chunk to send
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the peer
        s.connect(peer_addr)
        
        # Read the chunk data from the local file
        with open(f'chunks/chunk_{chunk_index}.dat', 'rb') as f:
            chunk_data = f.read()

        # Create message with chunk metadata and data
        message = {
            'chunk_index': chunk_index,
            'chunk_data': chunk_data
        }
        
        # Send serialized message to peer
        s.sendall(pickle.dumps(message))
        
        # Wait for acknowledgment from peer
        response = s.recv(1024)
        print(f"[Alice] Sent chunk {chunk_index} to {peer_addr}, got:", response.decode())

def register_with_tracker(file_id, chunk_map):
    """
    Registers information about chunks with the tracker.
    This allows others to find which peers have which chunks.
    
    Args:
        file_id: Identifier for the file (typically filename)
        chunk_map: Dictionary mapping chunk indices to peer addresses
    """
    for idx, peer in chunk_map.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Connect to tracker
                s.connect((TRACKER_HOST, TRACKER_PORT))
                
                # Create registration message
                message = {
                    'type': 'register',
                    'file_id': file_id,
                    'chunks': [idx],  # List of chunk indices this peer has
                    'peer_address': peer
                }
                
                # Send registration to tracker
                s.sendall(pickle.dumps(message))
                
                # Wait for acknowledgment
                _ = s.recv(1024)  # receive 'ok'
        except Exception as e:
            print(f"[ERROR] Failed to register chunk {idx} to tracker: {e}")


def run_alice():
    """Main function to run Alice's file sharing process"""
    # Get file path from user
    file_path = input("Enter path to file to share: ").strip()
    
    # Ensure directory for chunks exists
    os.makedirs('chunks', exist_ok=True)

    # Split the file into chunks using utility function
    total_chunks = split_file(file_path)
    
    # Use filename as the file_id for tracker
    file_id = os.path.basename(file_path)

    print(f"[Alice] File split into {total_chunks} chunks.")

    # Send chunks to peers and remember who got what
    chunk_map = {}
    for i in range(total_chunks):
        # Simple round-robin allocation of chunks to peers
        assigned_peer = PEERS[i % len(PEERS)]
        send_chunk_to_peer(assigned_peer, i)
        chunk_map[i] = assigned_peer

    # Register all chunks with the tracker
    register_with_tracker(file_id, chunk_map)
    print(f"[Alice] Registration with tracker complete.")

if __name__ == "__main__":
    run_alice()
