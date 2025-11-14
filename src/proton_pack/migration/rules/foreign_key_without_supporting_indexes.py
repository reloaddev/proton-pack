from typing import List

from sqlglot import exp


def check_for_foreign_key_without_supplementary_indexes(ast: List[exp.Expression]) -> List[exp.Expression]:
    unsafe = []

    fk_columns: set[exp.ForeignKey] = set()
    indexed_columns: set[exp.Index] = set()

    for tree in ast:
        for foreign_key in tree.find_all(exp.ForeignKey):
            operation = _find_operation(foreign_key)
            if type(operation) is exp.Create or type(operation) is exp.Alter:
                fk_columns.add(foreign_key)

        for index in tree.find_all(exp.Index):
            operation = _find_operation(index)
            if type(operation) is exp.Create or type(operation) is exp.Alter:
                indexed_columns.add(index)

    for fk_col in fk_columns:
        if len(indexed_columns) == 0:
            operation = _find_operation(fk_col)
            unsafe.append(operation)
        for index, indexed_col in enumerate(indexed_columns):
            if _is_matching_columns(indexed_col, fk_col):
                break
            if not _is_matching_columns(indexed_col, fk_col) and index == len(indexed_columns) - 1:
                operation = _find_operation(fk_col)
                unsafe.append(operation)

    return unsafe


def _is_matching_columns(indexed_col: exp.Index, referencing_col: exp.ForeignKey) -> bool:
    # 1st step: find indexed column names
    idx_params = indexed_col.find(exp.IndexParameters)
    idx_columns = [idx_params.args.get("columns")[i].name for i, x in enumerate(idx_params.args.get("columns"))]

    # 2nd step: find referenced column names
    referencing_columns = []
    referencing_col_expressions = referencing_col.args.get("expressions")
    if referencing_col_expressions:
        for expr in referencing_col_expressions:
            ident = expr if isinstance(expr, exp.Identifier) else expr.find(exp.Identifier)
            if ident:
                referencing_columns.append(ident.name)

    # 2nd step: fallback solution
    referencing_columns = []
    for ident in referencing_col.find_all(exp.Identifier):
        if ident.find_ancestor(exp.Reference) is None:
            referencing_columns.append(ident.name)

    # 3rd step: match indexed and referencing columns
    for referencing_col in referencing_columns:
        if len(idx_columns) == 0:
            return False
        for index, indexed_col in enumerate(idx_columns):
            if referencing_col == indexed_col:
                break
            if index == len(idx_columns) - 1:
                return False

    # No referencing key
    return True


def _find_operation(node: exp.Expression) -> exp.Expression | None:
    create = node.find_ancestor(exp.Create)
    if create:
        return create

    alter = node.find_ancestor(exp.Alter)
    if alter:
        return alter

    drop = node.find_ancestor(exp.Drop)
    if drop:
        return drop

    return None
