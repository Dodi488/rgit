from main import ExecuteResult, BASE_PATH, BRANCH_NAME
from pathlib import Path
import os
import sys
import hashlib
import zlib
import struct
import hashlib
import binascii

sys.dont_write_bytecode = True

# Plumbing commands
def hash_object(file: str, t: str, w: bool, stdin: bool, stdin_paths: bool, path: str, no_filters: bool, literally: bool) -> list[str]:
    if stdin:
        input_data = sys.stdin.buffer.read()
    elif file:
        input_data = Path(file).read_bytes()
    else:
        print("Provide a file or use --stdin")

    header = f"{t} {len(input_data)}\0".encode("utf-8")
    data = header + input_data

    hash = hashlib.sha1(data).hexdigest()
    print(hash)

    if w:
        file_path = f"{BASE_PATH}/objects/{hash[:2]}/{hash[2:]}"
        final_path = Path(file_path)
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_data = zlib.compress(data)
        final_path.write_bytes(final_data)

    return hash

def cat_file(e: bool, p: bool, t: bool, s: bool, textconv: bool, filters: bool, batch: bool, batch_check: bool, batch_command: bool, batch_all_objects: bool, buffer: bool, follow_symlinks: bool, unordered: bool, Z: bool, objects: list[str]):
    is_mode_2 = any([e, p, t, s])

    if is_mode_2:
        if len(objects) != 1:
            print("fatal: -e, -p, -t, -s require exactly one <object> argument.")
            exit()

        hash = objects[0]
        
        def check_object_type(hash: str) -> tuple(str, str):
            with open(f"{BASE_PATH}/objects/{hash[:2]}/{hash[2:]}", "rb") as f:
                file = f.read()

            decompressed = zlib.decompress(file)
            file_type = decompressed[0:6].decode("utf-8")

            return file_type, decompressed

        def is_tree(bytes: bytes) -> str:
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

        def is_commit(bytes: bytes) -> str:
            with open(f"{BASE_PATH}/objects/{bytes[:2]}/{bytes[2:]}", "rb") as f:
                file = f.read()
            decompress = zlib.decompress(file)
            raw_data = decompress.split(b"\x00")[1]
            data = repr(raw_data)[2:-1]
            final = data.replace(r"\n", "\n")

            return final[:-1]

        def is_blob(decompressed) -> str:
            final = decompressed.decode("utf-8").split("\x00")
            return final
            
        if hash == "HEAD^{{tree}}":
            with open(f"{BASE_PATH}/HEAD", "r") as f:
                file = f.read()

            new_path = file[5:-1]
            with open(f"{BASE_PATH}/{new_path}", "rb") as f:
                file = f.read()

            commit_hash = is_commit(file[:-1])[-40:]
            commit_hash = commit_hash.replace("\n", " ").split(" ")
            hash = commit_hash[1]

        if hash == f"{BRANCH_NAME}^{{tree}}":
            with open(f"{BASE_PATH}/refs/heads/{BRANCH_NAME}", "r") as f:
                file = f.read()

            commit_hash = is_commit(file[:-1])#[-40:]
            commit_hash = commit_hash.replace("\n", " ").split(" ")
            hash = commit_hash[1]

        if e:
            # Implement logic to check if its blob, commit, tree or tag. look at that header, automatically figure out the content type, strip the metadata, and cleanly output just the original contents.
            pass

        elif p:
            # Implement logic to check if its blob, commit, tree or tag. look at that header, automatically figure out the content type, strip the metadata, and cleanly output just the original contents.
            file_type, content = check_object_type(hash)

            if file_type[0:4] == "blob":
                file_content = is_blob(content)[1].replace("\n", "")
            elif file_type[0:4] == "tree":
                #content = content.replace(b"\x00", b" 0").split(b" ")
                #content = content[2:-1].split(b" ")[1:]
                file_content = is_tree(content)
            elif file_type == "commit":
                file_content = is_commit(hash)

            return file_content

        elif t:
            # Implement logic to check if its blob, commit, tree or tag. look at that header, automatically figure out the content type, strip the metadata, and cleanly output just the original contents.
            file_type, content = check_object_type(hash)

            if file_type[0:4] == "blob":
                file_type = "blob"
            elif file_type[0:4] == "tree":
                file_type = "tree"
            elif file_type == "commit":
                file_type = "commit"

            return file_type

    elif batch or batch_check or batch_command:
        if len(objects) > 0:
            parser.error("Batch modes do not take positional arguments.")

    elif textconv or filters:
        pass

    else:
        if len(objects) != 2:
            parser.error("Requires exactly 2 arguments <type> <object>.")
        obj_type, target_object = objects

    return

def update_index(
    add: bool = False,
    remove: bool = False,
    force_remove: bool = False,
    replace: bool = False,
    refresh: bool = False,
    q: bool = False,
    unmerged: bool = False,
    ignore_missing: bool = False,
    cacheinfo: list[list[str]] | None = None,
    chmod: str | None = None,
    assume_unchanged: bool = False,
    no_assume_unchanged: bool = False,
    skip_worktree: bool = False,
    no_skip_worktree: bool = False,
    ignore_skip_worktree_entries: bool = False,
    no_ignore_skip_worktree_entries: bool = False,
    fsmonitor_valid: bool = False,
    no_fsmonitor_valid: bool = False,
    ignore_submodules: bool = False,
    split_index: bool = False,
    no_split_index: bool = False,
    untracked_cache: bool = False,
    no_untracked_cache: bool = False,
    test_untracked_cache: bool = False,
    force_untracked_cache: bool = False,
    fsmonitor: bool = False,
    no_fsmonitor: bool = False,
    really_refresh: bool = False,
    unresolve: bool = False,
    again: bool = False,
    info_only: bool = False,
    index_info: bool = False,
    z: bool = False,
    stdin: bool = False,
    index_version: int | None = None,
    show_index_version: bool = False,
    verbose: bool = False,
    files: list[str] | None = None
) -> str:
    if not files:
        return "No files specified"

    index_path = Path(f"{BASE_PATH}/index")
    entries = {}

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

    for file_path in files:
        target_file = Path(file_path)
        if not target_file.exists():
            print(f"fatal: pathspec '{file_path}' did not match any files")
            continue

        content = target_file.read_bytes()
        header = f"blob {len(content)}\0".encode("utf-8")
        store_data = header + content
        
        sha1 = hashlib.sha1(store_data)
        hash_digest = sha1.digest()
        hash_hex = sha1.hexdigest()
        
        blob_path = Path(f"{BASE_PATH}/objects/{hash_hex[:2]}/{hash_hex[2:]}")
        blob_path.parent.mkdir(parents=True, exist_ok=True)
        blob_path.write_bytes(zlib.compress(store_data))

        st = target_file.stat()
        ctime_s = int(st.st_ctime) & 0xFFFFFFFF
        ctime_ns = int(st.st_ctime_ns % 1_000_000_000) & 0xFFFFFFFF
        mtime_s = int(st.st_mtime) & 0xFFFFFFFF
        mtime_ns = int(st.st_mtime_ns % 1_000_000_000) & 0xFFFFFFFF
        dev = int(st.st_dev) & 0xFFFFFFFF
        ino = int(st.st_ino) & 0xFFFFFFFF
        uid = int(st.st_uid) & 0xFFFFFFFF
        gid = int(st.st_gid) & 0xFFFFFFFF
        size = int(st.st_size) & 0xFFFFFFFF

        mode = 0o100755 if os.access(target_file, os.X_OK) else 0o100644
        
        name_bytes = str(target_file).encode("utf-8")
        flags = len(name_bytes) & 0x0FFF

        entry_meta = struct.pack(">10I20sH", 
            ctime_s, ctime_ns, mtime_s, mtime_ns, dev, ino, mode, uid, gid, size,
            hash_digest, flags
        )
        
        entry_without_padding = entry_meta + name_bytes
        pad_len = 8 - (len(entry_without_padding) % 8)
        new_entry = entry_without_padding + (b"\x00" * pad_len)
        
        entries[name_bytes] = new_entry

    sorted_names = sorted(entries.keys())
    new_header = struct.pack(">4sII", b"DIRC", 2, len(sorted_names))
    
    index_content = bytearray(new_header)
    for name in sorted_names:
        index_content.extend(entries[name])
        
    checksum = hashlib.sha1(index_content).digest()
    index_path.write_bytes(index_content + checksum)

    return

def write_tree(missing_ok: bool=False, prefix: str | None = None) -> str:
    if not missing_ok:
        if not Path(f"{BASE_PATH}/index").is_file():
            print("There is no index file or is corrupt.")

    # This logic is wrong, what this flag does is from all the files in index it chooses one to save into .git/objects.
    if prefix == None:
        path = f"{BASE_PATH}/index"
    else:
        path = f"{BASE_PATH}/{prefix}/*" # Here is not like this, I have to write all including subdirectories. I know the syntax is wrong but to have an idea.

    with open(path, "rb") as f:
        index_bytes = f.read()
        
    hashed_tree = hash_tree(index_bytes)
    return hashed_tree
    
def read_tree(
    m: bool = False,
    trivial: bool = False,
    aggressive: bool = False,
    reset: bool = False,
    prefix: str | None = None,
    u: bool = False,
    i: bool = False,
    index_output: str | None = None,
    no_sparse_checkout: bool = False,
    empty: bool = False,
    tree_ish: list[str] | None = None
) -> None:
    index_path = Path(f"{BASE_PATH}/index")
 
    data = index_path.read_bytes()
    num_entries = int.from_bytes(data[8:12], "big")
    offset = 12
    entries = []
 
    for _ in range(num_entries):
        mode = int.from_bytes(data[offset + 24:offset + 28], "big")
        raw_hash = data[offset + 40:offset + 60]
        path_end = data.find(b"\x00", offset + 62)
        name = data[offset + 62:path_end]
        entry_len = 62 + len(name)
        offset += entry_len + (8 - entry_len % 8)
        entries.append((mode, raw_hash, name))
 
    if prefix:
        p = prefix.rstrip("/").encode() + b"/"
        entries = [(m, h, n[len(p):]) for m, h, n in entries if n.startswith(p)]
        if not entries:
            raise SystemExit(f"fatal: prefix {prefix} not found in index")
 
    return hash_tree(entries).hex()
