from typing import List

from sqlglot import exp

def check_for_drop_columns(ast: List[exp.Expression]) -> bool:
    for tree in ast:
        if tree.find(exp.Drop) is not None:
            return True
    return False