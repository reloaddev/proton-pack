from typing import List

from sqlglot import exp

def check_for_drop_columns(ast: List[exp.Expression]) -> List[exp.Expression]:
    unsafe = []

    for tree in ast:
        drop = tree.find(exp.Drop)
        if drop is not None:
            kind = drop.args.get("kind")
            if kind == "TABLE":
                unsafe.append(drop)
            elif kind == "COLUMN":
                alter = drop.find_ancestor(exp.Alter)
                unsafe.append(alter)

    return unsafe