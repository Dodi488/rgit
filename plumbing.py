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
    # We have to check if the files are in the index, for now I will just assume that its not.
    print(files)
    path = f"{BASE_PATH}/index"
    #path = Path(path)

    if cacheinfo:
        if len(cacheinfo) != 0:
            mode = cacheinfo[0][0].encode()
            hash = cacheinfo[0][1].encode()
            name = cacheinfo[0][2].encode()

    else:
        mode = oct(os.stat(files[0]).st_mode)
        
        if mode == "040000":
            t = "tree"
        elif mode == "160000":
            t = "commit"
        else:
            t = "blob"

        with open(files[0], "rb") as f:
            input_data = f.read()
        header = f"{t} {len(input_data)}\0".encode("utf-8")
        data = header + input_data

        hash = hashlib.sha1(data).hexdigest()

        name = files[0].encode()

    if add:
        header = struct.pack("!4sII", b"DIRC", 2, 1)

        # We have to define the timestapms later.
        ctime_s = ctime_ns = mtime_s = mtime_ns = 0
        dev = ino = uid = gid = file_size = 0

        if not isinstance(mode, int):
            mode = int(mode, 8)

        entry_meta = struct.pack("!10I", ctime_s, ctime_ns, mtime_s, mtime_ns, dev, ino, mode, uid, gid, file_size)

        hash = binascii.unhexlify(hash)
        print(hash)

        name_lenght = len(name)
        flags = struct.pack("!H", name_lenght)

        entry_len = 62 + name_lenght
        padding_len = 8 - (entry_len % 8)
        padding = b"\x00" * padding_len

        data = entry_meta + hash + flags + name + padding

        index = header + data
        checksum = hashlib.sha1(index).digest()

        final = index + checksum

        print(final)
        print(type(final))
        print(path)
        print(type(path))

        with open(path, "ab") as f:
            f.write(final)

    return "done"

def write_tree(missing_ok: bool=False, prefix: str | None = None) -> str:
    if not missing_ok:
        if not Path(f"{BASE_PATH}/index").is_file():
            print("There is no index file or is corrupt.")

    if prefix == None:
        path = f"{BASE_PATH}/index"
    else:
        path = f"{BASE_PATH}/{prefix}/*" # Here is not like this, I have to write all including subdirectories. I know the syntax is wrong but to have an idea.

    with open(path, "rb") as f:
        index_bytes = f.read()

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
