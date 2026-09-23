from porcelin import *
import sys
from pathlib import Path
from enum import Enum

class ExecuteResult(Enum):
    EXECUTE_SUCCESS = 0
    EXECUTE_FAIL = 1

class SyntaxStatus(Enum):
    SYNTAX_CORRECT = 0
    SYNTAX_ERROR = 1

def prepare_init(*args: Tuple) -> SyntaxStatus:
    list(args)
    if len(args) <= 2:
        print("You must select a directory when using init.")
        return SyntaxStatus.SYNTAX_FAIL

    dir = next((item for item in args if not item.startswith("--")), None)
        print("You must select a directory when using init.")
        return SyntaxStatus.SYNTAX_FAIL

    args.pop(dir)
    init(dir, args)
    return SyntaxStatus.SYNTAX_CORRECT

def execute(command):
    handler = porcelin_commands.get(command, handle_unrecognized)
    return handler()

def main():
    if len(sys.argv) < 2:
        print("Error.")


    command = sys.argv[1]

    porcelin_commands = {
        "init": prepare_init,
        "add": prepare_add
    }

    match execute(command):
        case SyntaxStatus.SYNTAX_CORRECT or ExecuteResult.EXECUTE_SUCCESS:
            pass
        case SyntaxStatus.SYNTAX_ERROR or ExecuteResult.EXECUTE_FAIL:
            pass
