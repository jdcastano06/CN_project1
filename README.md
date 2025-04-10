# 📂 Hybrid File Sharing Application (Client-Server + P2P)

This project implements a **file-sharing application** using a **hybrid architecture** combining client-server and peer-to-peer (P2P) models. It is built entirely in **plain Python** using `socket` and `threading`, without external frameworks.

---

## Features
- File chunking and distributed storage.
- Peers store and serve chunks.
- Central tracker for metadata and peer coordination.
- Reconstructs the original file from chunks via peer retrieval.

---

## Architecture Overview

```
   [ Alice (Uploader) ]
          |
     [ Splits File ]
          |
     Sends Chunks to
   /                    \
[Peer 1]            [Peer 2]
   \                    /
    \                /
     [  Tracker  ] <--- Alice registers chunk info
          |
      Bob requests chunk map
          |
       [ Bob (Downloader) ]
          |
     Contacts peers to get chunks
          |
     Reconstructs original file
```

---

## Folder Structure
```
file_sharing_app/
├── tracker.py         # Metadata registry (client-server component)
├── peer.py            # Peer node storing/serving chunks
├── alice.py           # Uploads, splits, and sends file chunks
├── bob.py             # Downloads and reconstructs files
├── utils.py           # File split/reconstruction helpers
├── generate_big_file.py  # For generating test files
├── chunks/            # Temp chunk storage from Alice
├── peer_9101_storage/ # Peer 1's chunk storage
├── peer_9102_storage/ # Peer 2's chunk storage
├── bob_chunks/        # Where Bob stores downloaded chunks
```

---

## How to Run It

### 1. Generate a Test File (optional)
```bash
python generate_big_file.py  # Creates big_test_file.txt (~50MB)
```

### 2. Start the Tracker (Terminal 1)
```bash
python tracker.py
```

### 3. Start Peers (Terminal 2 & 3)
```bash
python peer.py 9101
python peer.py 9102
```

### 4. Run Alice to Upload File (Terminal 4)
```bash
python alice.py
# Enter: big_test_file.txt
```

### 5. Run Bob to Download File (Terminal 5)
```bash
python bob.py
# Enter: big_test_file.txt
```

---

## Key Components Explained

### tracker.py
- Keeps track of which peer holds which file chunks.
- Supports `register` (from Alice) and `get_peers` (from Bob).
- Simple socket server handling one request per connection.

### peer.py
- Listens for connections from Alice and Bob.
- Stores chunks on disk when Alice uploads.
- Sends requested chunks to Bob.
- Uses `reliable_recv()` to handle partial TCP data.

### alice.py
- Splits file using `utils.split_file()`.
- Sends chunks alternately to peers (round-robin).
- Notifies tracker about which peer got which chunk.

### bob.py
- Requests chunk-to-peer mapping from tracker.
- Connects to relevant peers to download chunks.
- Reconstructs file using `utils.reconstruct_file()`.

---

## Notes
- All connections use plain TCP with `socket`.
- Pickle is used for data serialization.
- Includes retry and error handling where necessary.
- Modular design allows easy peer expansion.

---

## Improvements (Optional)
- File hashing to ensure chunk integrity.
- Replication for fault tolerance.
- Web UI using Flask/FastAPI.
- Parallel downloading of chunks.

---

## Dependencies
- No external libraries required (only Python 3+)


