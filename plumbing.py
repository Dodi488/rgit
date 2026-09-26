from main import ExecuteResult, BASE_PATH, BRANCH_NAME
from pathlib import Path
import os
import sys
import hashlib
import zlib

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

        def is_tree(bytes: list[bytes]) -> str:
            header_end = bytes.find(b"\x00")
            content = bytes[header_end + 1:]
            lines = []

            while content:
                space = content.find(b" ")
                type = content[:space].decode("utf-8")

                nullo = content.find(b"\x00", space)
                name = content[space, + 1:nullo].decode("utf-8")

                sha = content[nullo + 1:nullo + 21]

                type = mode.zfill(6)

                if type == "040000":
                    t = "tree"
                elif type == "160000":
                    t = "commit"
                else:
                    t = "blob"

            # for i in range(1, len(bytes)):
            #    line = bytes[i]
            #    last_line = bytes[i - 1]

            #    type = repr(last_line[-6:].replace(b"\x00", b"0"))[2:-1]
    
            #    if (i + 1) != len(bytes):
            #        name = repr(line[:-27])[2:-1]
            #        hash = line[-26:-6].hex()
            #    else:
            #        name = repr(line[:-20])[2:-1]
            #        hash = line[-26:].hex()

            #    if type == "040000":
            #        t = "tree"
            #    elif type == "160000":
            #        t = "commit"
            #    else:
            #        t = "blob"

                lines.append(f"{type} {t} {hash}    {name}")

                content = content[nullo + 21]
    
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
                content = content[2:-1].split(b" ")[1:]
                file_content = is_tree(content)
            elif file_type == "commit":
                file_content = is_commit(hash)

            return file_content

        elif t:
            # Implement logic to check if its blob, commit, tree or tag. look at that header, automatically figure out the content type, strip the metadata, and cleanly output just the original contents.
            file_type, content = check_object_type(hash)
            #file_type = is_blob(hash)[0].split(" ")[0]

            if file_type[0:4] == "blob":
                file_content = is_blob(content)[0].split(" ")[0]
            elif file_type[0:4] == "tree":
                file_content = is_tree(content[2:])
            else:
                pass # Implement this logic.

            return file_content

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
