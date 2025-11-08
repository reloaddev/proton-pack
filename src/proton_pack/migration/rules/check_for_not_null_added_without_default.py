from typing import List
from sqlglot import exp


def check_for_not_null_added_without_default(ast: List[exp.Expression]) -> bool:
    """
    Detect ALTER TABLE operations that add NOT NULL to an existing column without providing a DEFAULT.

    Risky pattern:
      - ALTER TABLE ... ALTER COLUMN ... SET NOT NULL (without a SET DEFAULT anywhere in the statement)

    Note: ADD COLUMN ... NOT NULL is allowed (safe at creation time), so it's ignored.
    """
    for tree in ast:
        for alter in tree.find_all(exp.Alter):
            sql = alter.sql(dialect="postgres").lower()

            # Flag when a statement sets NOT NULL but does not set any DEFAULT in the same ALTER.
            # (Heuristic; not per-column.)
            if " set not null" in sql and " set default" not in sql:
                return True

    return False