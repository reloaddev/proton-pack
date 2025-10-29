from typing import List
from sqlglot import exp


def check_for_not_null_constraints_dropped(ast: List[exp.Expression]) -> bool:
    """
    Detect ALTER TABLE ... DROP NOT NULL operations.

    Dropping a NOT NULL constraint can introduce unexpected NULLs into critical columns.
    """
    for tree in ast:
        alter = tree.find(exp.Alter)
        if alter is not None:
            if "drop not null" in alter.sql(dialect="postgres").lower():
                return True
    return False