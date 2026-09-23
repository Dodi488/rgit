from main import ExecuteResult, base_path
import pathlib as Path
import os
import sys
import zlib

def hash_object(
    *files: str,
    obj_type: str = "blob",
    write: bool = False,
    path: str | None = None,
    no_filters: bool = False,
    stdin: bool = False,
    literally: bool = False,
    stdin_paths: bool = False) -> list[str]:

    if stdid:
        input_data = sys.stdin.readline().encode("utf-8")
        print(input_data)

    header = f"blob {len(input_data)}\0".encode("utf-8)
    data = header + input_data

    hash = hashlib.sha1(data).hexdigest()

    if w:
        file_path = f"{base_path}{hash[:2]}/{hash[2:]}"
        final_path = Path(file_path)
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_data = zlib.compress(data)
        final_path.write_text(final_data)
