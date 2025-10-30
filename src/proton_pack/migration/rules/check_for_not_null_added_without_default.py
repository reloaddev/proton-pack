from typing import List
from sqlglot import exp


def check_for_not_null_added_without_default(ast: List[exp.Expression]) -> bool:
    """
    Detect ALTER TABLE operations that add NOT NULL without providing a DEFAULT.

    Risky patterns:
      - ALTER TABLE ... ALTER COLUMN ... SET NOT NULL (without a SET DEFAULT)
      - ALTER TABLE ... ADD COLUMN ... NOT NULL (without DEFAULT)
    """
    for tree in ast:
        # Check all ALTER TABLE statements
        for alter in tree.find_all(exp.Alter):
            sql = alter.sql(dialect="postgres").lower()

            # Heuristic checks within the same ALTER statement:
            # 1) SET NOT NULL without a SET DEFAULT
            if " set not null" in sql and " set default" not in sql:
                return True

            # 2) ADD COLUMN ... NOT NULL without DEFAULT
            if " add column " in sql and " not null" in sql and " default " not in sql:
                return True

    return False