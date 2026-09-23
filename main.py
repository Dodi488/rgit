#from porcelain import inint
import porcelain
import sys
from pathlib import Path
from enum import Enum

BASE_PATH = ".rgit"

class ExecuteResult(Enum):
    EXECUTE_SUCCESS = 0
    EXECUTE_FAIL = 1

class SyntaxStatus(Enum):
    SYNTAX_CORRECT = 0
    SYNTAX_ERROR = 1

def prepare_init(*args: Tuple) -> SyntaxStatus:
    list(args)
    print(args)
    if len(args) < 1:
        print("You must select a directory when using init.")
        return SyntaxStatus.SYNTAX_ERROR

    #dir = next((item for item in args if not item.startswith("--")), None)
    #    print("You must select a directory when using init.")
    #    return SyntaxStatus.SYNTAX_ERROR

    #args.pop(dir)
    porcelain.inint(dir, args[0])
    return SyntaxStatus.SYNTAX_CORRECT

def prepare_add():
    pass

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

    handler = porcelin_commands.get(command)
    match handler(sys.argv[2:]):
    #match execute(command):
        case SyntaxStatus.SYNTAX_CORRECT: #or ExecuteResult.EXECUTE_SUCCESS:
            sys.exit(SyntaxStatus.SYNTAX_ERROR.value)
        case SyntaxStatus.SYNTAX_ERROR: #or ExecuteResult.EXECUTE_FAIL:
            sys.exit(SyntaxStatus.SYNTAX_ERROR.value)

if __name__ == "__main__":
    main()
