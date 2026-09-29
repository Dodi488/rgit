from config import ExecuteResult, BASE_PATH, BRANCH_NAME
from pathlib import Path
import os
import sys
import hashlib
import zlib
import struct

sys.dont_write_bytecode = True

def unhash_tree(bytes: bytes) -> str:
    header_end = bytes.find(b"\x00")
    content = bytes[header_end + 1:]
    lines = []

    while content:
        space = content.find(b" ")
        type = content[:space].decode("utf-8")

        nullo = content.find(b"\x00", space)
        name = content[space + 1:nullo].decode("utf-8")

        hash = content[nullo + 1:nullo + 21]

        type = type.zfill(6)

        if type == "040000":
            t = "tree"
        elif type == "160000":
            t = "commit"
        else:
            t = "blob"

        lines.append(f"{type} {t} {hash.hex()}    {name}")

        content = content[nullo + 21:]

    return "\n".join(lines)

def hash_tree(index_bytes: bytes) -> str:
    num_entries = int.from_bytes(index_bytes[8:12], byteorder='big')
    offset = 12
    
    tree_entries = []

    for _ in range(num_entries):
        metadata = index_bytes[offset : offset + 62]
        
        mode_int = int.from_bytes(metadata[24:28], byteorder='big')
        mode_str = oct(mode_int)[2:] 
        
        raw_hash = metadata[40:60]
        
        path_start = offset + 62
        path_end = path_start
        while index_bytes[path_end] != 0x00:
            path_end += 1
            
        name = index_bytes[path_start:path_end] # Keep as raw bytes
        
        entry_size = 62 + (path_end - path_start)
        padding = 8 - (entry_size % 8)
        offset += entry_size + padding
        
        entry = mode_str.encode('utf-8') + b' ' + name + b'\x00' + raw_hash
        tree_entries.append((name, entry))

    tree_entries.sort(key=lambda x: x[0])
    tree_content = b"".join([entry[1] for entry in tree_entries])

    header = f"tree {len(tree_content)}\0".encode('utf-8')
    tree_object = header + tree_content

    tree_hash = hashlib.sha1(tree_object).hexdigest()

    file_path = Path(f"{BASE_PATH}/objects/{tree_hash[:2]}/{tree_hash[2:]}")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    final_data = zlib.compress(tree_object)
    file_path.write_bytes(final_data)

    return tree_hash
    
def read_hash(hash: str) -> bytes:
    if Path(f"{BASE_PATH}/objects/{hash[:2]}/{hash[2:]}").exists():
        with open(f"{BASE_PATH}/objects/{hash[:2]}/{hash[2:]}", "rb") as f:
            file = f.read()
        return file
    else:
        pass # Here is the logic to read from the files in objetcs (not hashes).

    # If all that fails, add a return statement that says that the hash does not exists.

def append_to_index(new_entries: dict[bytes, bytes]) -> None:
    index_path = Path(f"{BASE_PATH}/index")
    entries: dict[bytes, bytes] = {}

    if index_path.exists():
        data = index_path.read_bytes()
        if len(data) > 12:
            num_entries = struct.unpack(">I", data[8:12])[0]
            offset = 12
            for _ in range(num_entries):
                path_end = data.find(b'\x00', offset + 62)
                name_bytes = data[offset+62:path_end]
                
                entry_len = 62 + len(name_bytes)
                padding = 8 - (entry_len % 8)
                total_len = entry_len + padding
                
                entries[name_bytes] = data[offset:offset+total_len]
                offset += total_len

    entries.update(new_entries)

    sorted_names = sorted(entries.keys())
    new_header = struct.pack(">4sII", b"DIRC", 2, len(sorted_names))
    
    index_content = bytearray(new_header)
    for name in sorted_names:
        index_content.extend(entries[name])
        
    checksum = hashlib.sha1(index_content).digest()
    index_path.write_bytes(index_content + checksum)
