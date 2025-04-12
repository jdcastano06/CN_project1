import socket
import threading
import pickle
import os

def reliable_recv(sock):
    """
    Reliably receives potentially large serialized data over a socket.
    
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

def handle_client(conn, addr, storage_dir):
    """
    Handles client connections (either Alice sending chunks or Bob requesting chunks).
    
    Args:
        conn: Socket connection with the client
        addr: Address of the connected client
        storage_dir: Directory where chunks are stored
    """
    try:
        message = reliable_recv(conn)

        if 'chunk_data' in message:  # Alice sending a chunk
            chunk_index = message['chunk_index']
            chunk_data = message['chunk_data']

            # Store the received chunk
            with open(f"{storage_dir}/chunk_{chunk_index}.dat", 'wb') as f:
                f.write(chunk_data)

            print(f"[Peer] Stored chunk_{chunk_index}.dat from {addr}")
            conn.sendall(b"OK: chunk received")

        elif 'request_chunk' in message:  # Bob requesting a chunk
            chunk_index = message['request_chunk']
            file_path = f"{storage_dir}/chunk_{chunk_index}.dat"

            # Check if we have the requested chunk
            if os.path.exists(file_path):
                # Send the chunk data to Bob
                with open(file_path, 'rb') as f:
                    chunk_data = f.read()
                conn.sendall(pickle.dumps({'chunk_data': chunk_data}))
                print(f"[Peer] Sent chunk_{chunk_index}.dat to {addr}")
            else:
                # Report missing chunk
                conn.sendall(pickle.dumps({'error': 'Chunk not found'}))
                print(f"[Peer] Chunk {chunk_index} not found for {addr}")

    except Exception as e:
        print(f"[Peer] Error: {e}")
    finally:
        conn.close()

def run_peer(peer_port):
    """
    Main function to run a peer node.
    
    Args:
        peer_port: Port number on which to listen for connections
    """
    peer_host = 'localhost'
    # Create a unique storage directory for this peer based on its port
    storage_dir = f'peer_{peer_port}_storage'
    os.makedirs(storage_dir, exist_ok=True)

    # Set up the peer server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((peer_host, peer_port))
        s.listen()
        print(f"[Peer] Listening on {peer_host}:{peer_port}, storing in {storage_dir}")

        # Handle connections in a loop
        while True:
            conn, addr = s.accept()
            # Start a new thread for each client
            threading.Thread(target=handle_client, args=(conn, addr, storage_dir)).start()

if __name__ == "__main__":
    import sys
    # Use command-line argument for port or default to 9101
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9101
    run_peer(port)
