from typing import List

from sqlglot import exp

def check_for_foreign_key_without_supplementary_indexes(ast: List[exp.Expression]) -> bool:
    """
    Check AST for foreign key constraints without supplementary indexes.
    Setting a supplementary index on a foreign key constraint can yield better performance,
    e.g., for foreign key lookups.
    """
    is_foreign_key = False
    is_index = False
    for tree in ast:
        if tree.find(exp.ForeignKey) is not None:
            is_foreign_key = True
        if tree.find(exp.Index) is not None:
            is_index = True
    return is_foreign_key and not is_index