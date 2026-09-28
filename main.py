import sys
import argparse
from pathlib import Path
from typing import Tuple
import porcelin
import plumbing
from config import *

sys.dont_write_bytecode = True

# Helper functions
def parse_flags(name: str, flags: list, args: tuple):
    # Defina the name
    parser = argparse.ArgumentParser(prog=name)

    # Define the flags
    for flag in flags:
        flag_arg = flag.copy()
        name = flag_arg.pop("name")

        # Checks if there is an aliace
        if isinstance(name, list):
            parser.add_argument(*name, **flag_arg)
        else:
            parser.add_argument(name, **flag_arg)

    # Parse flags
    parsed_args = parser.parse_args(args)
    return parsed_args

# Porcelin commands
def prepare_init(*args) -> SyntaxStatus:
    if len(args) < 1:
        print("You must select a directory when using init.")
        return SyntaxStatus.SYNTAX_ERROR

    porcelin.init(dir=args[0])
    return SyntaxStatus.SYNTAX_CORRECT

def prepare_add():
    pass

# Plumbing commands
def prepare_hash_object(*args) -> str:
    possible_flags = [
        {"name": "file", "type": str, "nargs": "?", "help": "The file to hash"},
        {"name": "-t", "type": str, "default": "blob", "help": "Choose object file type."},
        {"name": "-w", "action": "store_true", "help": "Choose if you want to store the object."},
        {"name": "--stdin", "action": "store_true", "help": "Choose if you want your input from the standard input."},
        {"name": "--stdin-paths", "action": "store_true", "help": "Read filename from standard input."},
        {"name": "--path", "type": str, "help": "Hash object as if it were located at the given path."},
        {"name": "--no-filters", "action": "store_true", "help": "Hash the contents as is."},
        {"name": "--literally", "action": "store_true", "help": "Allow --stdin to hash any garbage."}
    ]

    parsed_args = parse_flags(name="hash-object", flags=possible_flags, args=args)
    
    final = plumbing.hash_object(**vars(parsed_args))
    return SyntaxStatus.SYNTAX_CORRECT, final

def prepare_cat_file(*args) -> SyntaxStatus:
    possible_flags = [
        {"name": "-e", "action": "store_true", "help": "Exit with zero status if <object> is valid, if its not exit with non zero status."},
        {"name": "-p", "action": "store_true", "help": "Prety-print the contents of <object> based in its type."},
        {"name": "-t", "action": "store_true", "help": "Show <object> file."},
        {"name": "-s", "action": "store_true", "help": "Show the size of <object>. If used with --use-mailmap it will show the size of updated object after being replace with idents using the mailmap mechanism."},
        {"name": "--textconv", "action": "store_true", "help": "Show the content as transformed by a textconv filter."},
        {"name": "--filters", "action": "store_true", "help": "Show the content as converted by the filters configured in the current working tree for the given <path>."},
        {"name": "--batch", "action": "store_true", "help": "Print object information and contents for each object in stdin."},
        {"name": "--batch-check", "action": "store_true", "help": ""},
        {"name": "--batch-command", "action": "store_true", "help": ""},
        {"name": "--batch-all-objects", "action": "store_true", "help": ""},
        {"name": "--buffer", "action": "store_true", "help": ""},
        {"name": "--follow-symlinks", "action": "store_true", "help": ""},
        {"name": "--unordered", "action": "store_true", "help": ""},
        {"name": "-Z", "action": "store_true", "help": ""},
        {"name": "objects", "nargs": "*", "help": "<type> <object> OR <object> depending on flags"}
    ]

    parsed_args = parse_flags(name="cat_file", flags=possible_flags, args=args)

    final = plumbing.cat_file(**vars(parsed_args))

    print(final)
    return SyntaxStatus.SYNTAX_CORRECT

def prepare_update_index(*args) -> SyntaxStatus:
    possible_flags = [
        {"name": "--add", "action": "store_true"},
        {"name": "--remove", "action": "store_true"},
        {"name": "--force-remove", "action": "store_true"},
        {"name": "--replace", "action": "store_true"},
        {"name": "--refresh", "action": "store_true"},
        {"name": "-q", "action": "store_true"},
        {"name": "--unmerged", "action": "store_true"},
        {"name": "--ignore-missing", "action": "store_true"},
        {"name": "--cacheinfo", "nargs": 3, "action": "append", "help": "<mode>,<object>,<file>"},
        {"name": "--chmod", "type": str, "choices": ["+x", "-x"]},
        {"name": "--assume-unchanged", "action": "store_true"},
        {"name": "--no-assume-unchanged", "action": "store_true"},
        {"name": "--skip-worktree", "action": "store_true"},
        {"name": "--no-skip-worktree", "action": "store_true"},
        {"name": "--ignore-skip-worktree-entries", "action": "store_true"},
        {"name": "--no-ignore-skip-worktree-entries", "action": "store_true"},
        {"name": "--fsmonitor-valid", "action": "store_true"},
        {"name": "--no-fsmonitor-valid", "action": "store_true"},
        {"name": "--ignore-submodules", "action": "store_true"},
        {"name": "--split-index", "action": "store_true"},
        {"name": "--no-split-index", "action": "store_true"},
        {"name": "--untracked-cache", "action": "store_true"},
        {"name": "--no-untracked-cache", "action": "store_true"},
        {"name": "--test-untracked-cache", "action": "store_true"},
        {"name": "--force-untracked-cache", "action": "store_true"},
        {"name": "--fsmonitor", "action": "store_true"},
        {"name": "--no-fsmonitor", "action": "store_true"},
        {"name": "--really-refresh", "action": "store_true"},
        {"name": "--unresolve", "action": "store_true"},
        {"name": ["--again", "-g"], "action": "store_true"},
        {"name": "--info-only", "action": "store_true"},
        {"name": "--index-info", "action": "store_true"},
        {"name": "-z", "action": "store_true"},
        {"name": "--stdin", "action": "store_true"},
        {"name": "--index-version", "type": int, "help": "<n>"},
        {"name": "--show-index-version", "action": "store_true"},
        {"name": "--verbose", "action": "store_true"},
        {"name": "files", "nargs": "*", "help": "Files to update"}
    ]

    parsed_flags = parse_flags(name="update-index", flags=possible_flags, args=args)
    final = plumbing.update_index(**vars(parsed_flags))

    return SyntaxStatus.SYNTAX_CORRECT

def prepare_write_tree(*args) -> SyntaxStatus:
    possible_flags = [
        {"name": "--missing-ok", "action": "store_true"},
        {"name": "--prefix", "type": str, "help": "Writes a tree object that represents a subdirectory <prefix>. This can be used to write the tree object for a subproject that is in the named subdirectory."}
    ]

    parsed_flags = parse_flags(name="write-tree", flags=possible_flags, args=args)
    final = plumbing.write_tree(**vars(parsed_flags))
    print(final)

    return SyntaxStatus.SYNTAX_CORRECT

def prepare_read_tree(*args) -> SyntaxStatus:
    possible_flags = [
        {"name": "-m", "action": "store_true"},
        {"name": "--trivial", "action": "store_true"},
        {"name": "--aggressive", "action": "store_true"},
        {"name": "--reset", "action": "store_true"},
        {"name": "--prefix", "type": str},
        {"name": "-u", "action": "store_true"},
        {"name": "-i", "action": "store_true"},
        {"name": "--index-output", "type": str},
        {"name": "--no-sparse-checkout", "action": "store_true"},
        {"name": "--empty", "action": "store_true"},
        {"name": "tree_ish", "nargs": "*", "help": "<tree-ish1> [<tree-ish2> [<tree-ish3>]]"}
    ]

    parsed_flags = parse_flags(name="read-tree", flags=possible_flags, args=args)
    final = plumbing.read_tree(**vars(parsed_flags))
    
    if final:
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
        "cat-file": prepare_cat_file,
        "update-index": prepare_update_index,
        "write-tree": prepare_write_tree,
        "read-tree": prepare_read_tree
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
