import sys
import argparse
from pathlib import Path
from enum import Enum
from typing import Tuple

sys.dont_write_bytecode = True
BASE_PATH = ".rgit"
BRANCH_NAME = "main"

class ExecuteResult(Enum):
    EXECUTE_SUCCESS = 0
    EXECUTE_FAIL = 1

class SyntaxStatus(Enum):
    SYNTAX_CORRECT = 0
    SYNTAX_ERROR = 1

class PrepareArgs(Enum):
    SUCCESS = 0
    FAIL = 1

# Porcelin commands
import porcelin
def prepare_init(*args: Tuple) -> SyntaxStatus:
    if len(args) < 1:
        print("You must select a directory when using init.")
        return SyntaxStatus.SYNTAX_ERROR

    porcelin.init(dir=args[0])
    return SyntaxStatus.SYNTAX_CORRECT

def prepare_add():
    pass

# Plumbing commands
import plumbing
def prepare_hash_object(*args) -> tuple[SyntaxStatus, str]:
    # Define flags for hash-object
    parser = argparse.ArgumentParser(prog="hash-object")
    parser.add_argument("file", type=str, nargs="?", help="The file to hash")
    parser.add_argument("-t", type=str, default="blob", help="Choose object file type.")
    parser.add_argument("-w", action="store_true", help="Choose if you want to store the object.")
    parser.add_argument("--stdin", action="store_true", help="Choose if you want your input from the standard input.")
    parser.add_argument("--stdin-paths", action="store_true", help="Read filename from standard input.")
    parser.add_argument("--path", type=str, help="Hash object as if it were located at the given path.")
    parser.add_argument("--no-filters", action="store_true", help="Hash the contents as is.")
    parser.add_argument("--literally", action="store_true", help="Allow --stdin to hash any garbage.")

    parsed_args = parser.parse_args(args)
    
    final = plumbing.hash_object(**vars(parsed_args))
    return SyntaxStatus.SYNTAX_CORRECT, final

def prepare_cat_file(*args) -> SyntaxStatus:
    # Define flags
    parser = argparse.ArgumentParser(prog="cat_file")

    parser.add_mutually_exclusive_group()

    parser.add_argument("-e", action="store_true", help="Exit with zero status if <object> is valid, if its not exit with non zero status.")
    parser.add_argument("-p", action="store_true", help="Prety-print the contents of <object> based in its type.")
    parser.add_argument("-t", action="store_true", help="Show <object> file.")
    parser.add_argument("-s", action="store_true", help="Show the size of <object>. If used with --use-mailmap it will show the size of updated object after being replace with idents using the mailmap mechanism.")

    parser.add_argument("--textconv", action="store_true", help="Show the content as transformed by a textconv filter.")
    parser.add_argument("--filters", action="store_true", help="Show the content as converted by the filters configured in the current working tree for the given <path>.")

    parser.add_argument("--batch", action="store_true", help="Print object information and contents for each object in stdin.")
    parser.add_argument("--batch-check", action="store_true", help="")
    parser.add_argument("--batch-command", action="store_true", help="")
    parser.add_argument("--batch-all-objects", action="store_true", help="")

    parser.add_argument("--buffer", action="store_true", help="")
    parser.add_argument("--follow-symlinks", action="store_true", help="")
    parser.add_argument("--unordered", action="store_true", help="")
    parser.add_argument("-Z", action="store_true", help="")

    parser.add_argument("objects", nargs="*", help="<type> <object> OR <object> depending on flags")

    parsed_args = parser.parse_args(args)
    #args = parser.parse_args()

    final = plumbing.cat_file(**vars(parsed_args))

    #final = plumbing.cat_file(
    #    e=args.e,
    #    p=args.p,
    #    t=args.t,
    #    s=args.s,
    #    textconv=args.textconv,
    #    filters=args.filters,
    #    batch=args.batch,
    #    batch_check=args.batch_check,
    #    batch_command=args.batch_command,
    #    batch_all_objects=args.batch_all_objects,
    #    buffer=args.buffer,
    #    follow_symlinks=args.follow_symlinks,
    #    Z=args.Z,
    #    objects=args.objects
    #)

    print(final)
    return SyntaxStatus.SYNTAX_CORRECT

def main():
    if len(sys.argv) < 2:
        print("Error: missing command")
        sys.exit(1)

    command = sys.argv[1]
    arguments = sys.argv[2:]

    porcelin_commands = {
        "init": prepare_init,
        "add": prepare_add
    }

    plumbing_commands = {
        "hash-object": prepare_hash_object,
        "cat-file": prepare_cat_file
    }

    handler = porcelin_commands.get(command) or plumbing_commands.get(command)
    
    if not handler:
        print(f"Unknown command: {command}")
        sys.exit(1)

    return_value = handler(*arguments)

    status = return_value[0] if isinstance(return_value, tuple) else return_value

    match status:
        case SyntaxStatus.SYNTAX_CORRECT:
            sys.exit(SyntaxStatus.SYNTAX_CORRECT.value)
        case SyntaxStatus.SYNTAX_ERROR:
            sys.exit(SyntaxStatus.SYNTAX_ERROR.value)

if __name__ == "__main__":
    main()
