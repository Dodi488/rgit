import struct
from dataclasses import dataclass

@dataclass
class IndexEntry:
    ctime_s: int
    ctime_ns: int
    mtime_s: int
    mtime_ns: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha: bytes
    path: str

    _FMT = ">10I20sH"
    _META_SIZE = 62

    def to_bytes(self) -> bytes:
        name = self.path.encode("utf-8")
        flags = min(len(name), 0x0FFF)
        meta = struct.pack(
            self._FMT,
            self.ctime_s, self.ctime_ns, self.mtime_s, self.mtime_ns,
            self.dev, self.ino, self.mode, self.uid, self.gid, self.size,
            self.sha, flags,
        )
        entry = meta + name
        padding = 8 - (len(entry) % 8)
        return entry + b"\0" * padding

    @classmethod
    def from_bytes(cls, data: bytes, offset: int) -> tuple["IndexEntry", int]:
        """Parse one entry at offset. Returns (entry, offset_of_next_entry)."""
        fields = struct.unpack_from(cls._FMT, data, offset)
        *stat, sha, _flags = fields
        path_start = offset + cls._META_SIZE
        path_end = data.index(b"\0", path_start)
        path = data[path_start:path_end].decode("utf-8")

        entry_len = cls._META_SIZE + (path_end - path_start)
        next_offset = offset + entry_len + (8 - entry_len % 8)
        return cls(*stat, sha, path), next_offset
        
def read_index() -> dict[str, IndexEntry]:
    path = Path(BASE_PATH) / "index"
    if not path.exists():
        return {}
    data = path.read_bytes()
    count = struct.unpack_from(">I", data, 8)[0]
    entries, offset = {}, 12
    for _ in range(count):
        entry, offset = IndexEntry.from_bytes(data, offset)
        entries[entry.path] = entry
    return entries

def write_index(entries: dict[str, IndexEntry]) -> None:
    body = struct.pack(">4sII", b"DIRC", 2, len(entries))
    body += b"".join(entries[p].to_bytes() for p in sorted(entries))
    checksum = hashlib.sha1(body).digest()
    (Path(BASE_PATH) / "index").write_bytes(body + checksum)
