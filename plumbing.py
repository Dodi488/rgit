from main import ExecuteResult, BASE_PATH
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

        if e:
            pass

        elif p:
            # Implement logic to check if its blob, commit, tree or tag. look at that header, automatically figure out the content type, strip the metadata, and cleanly output just the original contents.
            with open(f"{BASE_PATH}/objects/{hash[:2]}/{hash[2:]}", "rb") as f:
                file = f.read()
            return zlib.decompress(file)
        
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
