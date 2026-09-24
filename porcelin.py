from main import ExecuteResult, BASE_PATH
import sys
from pathlib import Path

sys.dont_write_bytecode = True

def init(dir: str, flags: list | None = None) -> None:
    Path(f"{BASE_PATH}/objects/info").mkdir(parents=True, exist_ok=True)
    Path(f"{BASE_PATH}/objects/pack").mkdir(parents=True, exist_ok=True)
    Path(f"{BASE_PATH}/refs").mkdir(exist_ok=True)
    Path(f"{BASE_PATH}/HEAD").touch()
    # Path(f"{BASE_PATH}/index").touch()
