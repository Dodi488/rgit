from config import BASE_PATH
from pathlib import Path
import hashlib
import zlib

def object_path(hash: str) -> Path:
    path = Path(f"{BASE_PATH}/objects/{hash[:2]}/{hash[2:]}")

    return path

def write_object(obj_type: str, data: bytes) -> str:
    raw = f"{obj_type} {len(data)}\0".encode() + data
    sha = hashlib.sha1(raw).hexdigest()
    path = object_path(sha)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(zlib.compress(raw))

    return sha

def read_object(sha: str) -> tuple[str, bytes]:
    raw = zlib.decompress(object_path(sha).read_bytes())
    header, _, data = raw.partition(b"\0")
    obj_type, _, _size = header.partition(b" ")

    return obj_type.decode(), data
