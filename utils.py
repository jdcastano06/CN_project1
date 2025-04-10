import os

def split_file(file_path, chunk_size=1024*512):  # 512 KB chunks
    with open(file_path, 'rb') as f:
        chunk_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            with open(f'chunks/chunk_{chunk_num}.dat', 'wb') as cf:
                cf.write(chunk)
            chunk_num += 1
    return chunk_num  # Total number of chunks created
