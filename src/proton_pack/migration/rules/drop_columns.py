from typing import List

from sqlglot import exp

def check_for_drop_columns(ast: List[exp.Expression]) -> bool:
    for tree in ast:
        drop = tree.find(exp.Drop)
        if drop is not None:
            kind = drop.args.get("kind")
            if kind == "TABLE" or kind == "COLUMN":
                return True
    return False