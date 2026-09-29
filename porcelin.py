from config import ExecuteResult, BASE_PATH, BRANCH_NAME
import sys
from pathlib import Path

sys.dont_write_bytecode = True

def init(dir: str, flags: list | None = None) -> None:
    Path(f"{BASE_PATH}/objects/info").mkdir(parents=True, exist_ok=True)
    Path(f"{BASE_PATH}/objects/pack").mkdir(parents=True, exist_ok=True)
    Path(f"{BASE_PATH}/refs/heads").mkdir(parents=True, exist_ok=True)
    Path(f"{BASE_PATH}/refs/heads/{BRANCH_NAME}").touch() # When the first commit is done, here we are going to write the sha-1 of the object.
    Path(f"{BASE_PATH}/HEAD").write_text(f"ref: refs/heads/{BRANCH_NAME}\n", encoding="utf-8")
    # Path(f"{BASE_PATH}/index").touch()
