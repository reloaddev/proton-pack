from typing import Dict
from sqlglot import exp

from proton_pack.migration.rules.drop_columns import check_for_drop_columns


def analyze_ast(ast: exp.Expression) -> Dict[str, bool]:
    """
    Analyze a sqlglot AST for potentially dangerous operations.

    Current checks:
      - DROP_DETECTED: True if any DROP statement is present anywhere in the tree.
    """
    return {"DROP_DETECTED": check_for_drop_columns(ast)}
