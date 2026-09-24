import sys
from pathlib import Path
from enum import Enum
import argparse
from typing import Tuple

sys.dont_write_bytecode = True
#parser = argparse.ArgumentParser()
BASE_PATH = ".rgit"

class ExecuteResult(Enum):
    EXECUTE_SUCCESS = 0
    EXECUTE_FAIL = 1

class SyntaxStatus(Enum):
    SYNTAX_CORRECT = 0
    SYNTAX_ERROR = 1

class PrepareArgs(Enum):
    SUCCESS = 0
    FAIL = 1

# Porcelin commands:
import porcelin
def prepare_init(*args: Tuple) -> SyntaxStatus:
    list(args)
    if len(args) < 1:
        print("You must select a directory when using init.")
        return SyntaxStatus.SYNTAX_ERROR

    #dir = next((item for item in args if not item.startswith("--")), None)
    #    print("You must select a directory when using init.")
    #    return SyntaxStatus.SYNTAX_ERROR

    #args.pop(dir)
    porcelin.inint(dir, args[0])
    return SyntaxStatus.SYNTAX_CORRECT

def prepare_add():
    pass

import plumbing
# Plumbing commands:
def prepare_hash_object(*args: Tuple) -> tuple(SyntaxStatus, ExecuteResult):
    #args, status = prepare_arguments(args, n=2)

    print(args)
    t = "-t" in args
    w = "-w" in args
    stdin = "--stdin" in args
    stdin_paths = "--stdin_path" in args
    path = "." if "--path" in args else "."
    no_filters = "--no-filters" in args
    literally = "--literally" in args

    #if status == PrepareArgs.FAIL:
    #    sys.exit(SyntaxStatus.SYNTAX_ERROR.value)

    # Define flags for hash-object
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, nargs="?", help="The file to hash")
    parser.add_argument("-t", type=str, default="blob", help="Choose object file type.")
    parser.add_argument("-w", action="store_true", default=False, help="Choose if you want to store the object.")
    parser.add_argument("--stdin", action="store_true", default=False, help="Choose if you want your input from the standard input.")
    parser.add_argument("--stdin-paths", action="store_true", default=False, help="Read filename from the standard input.")
    parser.add_argument("--path", type=str, help="Hash object as if it were located at the given path.")
    parser.add_argument("--no-filters", action="store_true", default=False, help=".Hash the contents as is, ignoring any input filter that would have been chosen by the attributes mechanism, including the end-of-line conversion")
    parser.add_argument("--literally", action="store_true", default=False, help="Allow --stdin to hash any garbage into a loose object which might not otherwise pass standard object parsing or git-fsck checks.")

    args = parser.parse_args()
    final = plumbing.hash_object(t, w, stdin, stdin_paths, path, no_filters, literally)
    print(final)
    return SyntaxStatus.SYNTAX_CORRECT, final

# Helper execute function
def prepare_arguments(*args: tuple, n: int) -> tuple[list[str], PrepareArgs]:
    if len(args) < n:
        return list("0"), PrepareArgs.FAIL
    else:
        return list(args), PrepareArgs.SUCCESS

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

    plumbing_commands = {
        "hash-object": prepare_hash_object
    }

    handler = porcelin_commands.get(command) or plumbing_commands.get(command)
    arguments = sys.argv[2:]
    print(*arguments)
    #print(type(*arguments))
    return_value = handler(*arguments)
    print(return_value)
    print(type(return_value))
    match return_value:
    #match execute(command):
        case SyntaxStatus.SYNTAX_CORRECT: #or ExecuteResult.EXECUTE_SUCCESS:
            sys.exit(SyntaxStatus.SYNTAX_CORRECT.value)
        case SyntaxStatus.SYNTAX_ERROR: #or ExecuteResult.EXECUTE_FAIL:
            sys.exit(SyntaxStatus.SYNTAX_ERROR.value)

if __name__ == "__main__":
    main()
