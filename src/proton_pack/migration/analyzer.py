from typing import Dict, List
from sqlglot import exp

from proton_pack.migration.rules.drop_columns import check_for_drop_columns
from proton_pack.migration.rules.foreign_key_without_supporting_indexes import check_for_foreign_key_without_supplementary_indexes


def analyze_ast(ast: List[exp.Expression]) -> Dict[str, bool]:
    """
    Analyze a sqlglot AST for potentially dangerous operations.

    Current checks:
      - DROP_DETECTED: True if any DROP statement is present anywhere in the tree.
    """
    return {
        "DROP_DETECTED": check_for_drop_columns(ast),
        "FOREIGN_KEY_WITHOUT_SUPP_INDEX": check_for_foreign_key_without_supplementary_indexes(ast)
    }
