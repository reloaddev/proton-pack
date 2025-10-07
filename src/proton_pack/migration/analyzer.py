from typing import Dict
from sqlglot import exp


def analyze_ast(ast: exp.Expression) -> Dict[str, bool]:
    """
    Analyze a sqlglot AST for potentially dangerous operations.

    Current checks:
      - DROP_DETECTED: True if any DROP statement is present anywhere in the tree.
    """
    drop_detected = ast.find(exp.Drop) is not None
    return {"DROP_DETECTED": drop_detected}
