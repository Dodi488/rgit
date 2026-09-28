from config import ExecuteResult, BASE_PATH, BRANCH_NAME
import sys
from pathlib import Path

sys.dont_write_bytecode = True

def init(dir: str, flags: list | None = None) -> None:
    Path(f"{BASE_PATH}/objects/info").mkdir(parents=True, exist_ok=True)
    Path(f"{BASE_PATH}/objects/pack").mkdir(parents=True, exist_ok=True)
    Path(f"{BASE_PATH}/refs/head/{BRANCH_NAME}").mkdir(exist_ok=True)
    Path(f"{BASE_PATH}/HEAD").touch()
    Path(f"{BASE_PATH}/HEAD").write_text("ref: refs/heads/{BRANCH_NAME}\n", encoding="utf-8")
    # Path(f"{BASE_PATH}/index").touch()
