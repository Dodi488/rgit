from main import ExecuteStatus
import sys
from pathlib import Path

def init(dir: str, flags: list) -> None:
    Path("objects/info").mkdir(parents=True, exist_ok=True)
    Path("objects/pack").mkdir(parents=True, exist_ok=True)
    Path("refs").mkdir(exist_ok=True)
    Path("HEAD").touch()
    # Path("index").touch()

if "__name__" == __main__:
    # IDK
    pass
