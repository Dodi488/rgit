import sys
from enum import Enum

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
