from typing import List

from sqlglot import exp


def check_for_foreign_key_without_supplementary_indexes(ast: List[exp.Expression]) -> bool:
    Key = tuple[str, tuple[str, ...]]
    fk_columns: set[Key] = set()
    indexed_columns: set[Key] = set()

    for tree in ast:
        foreign_keys = tree.find_all(exp.ForeignKey)
        for foreign_key in foreign_keys:
            table = _find_table_for(foreign_key)
            if not table:
                continue
            referencing_cols = _find_referencing_columns_for(foreign_key)
            if not referencing_cols:
                continue
            col_tuple: tuple[str, ...] = tuple(c.lower() for c in referencing_cols)
            fk_columns.add((table["name"], col_tuple))

        for index in tree.find_all(exp.Index):
            table = _find_table_for(index)
            if not table:
                continue
            indexed_cols = _find_indexed_columns_for(index)
            if not indexed_cols:
                continue
            col_tuple: tuple[str, ...] = tuple(c.lower() for c in indexed_cols)
            indexed_columns.add((table["name"], col_tuple))

    if len(fk_columns) == 0 and len(indexed_columns) == 0:
        return False

    for fk_col in fk_columns:
        for indexed_col in indexed_columns:
            if fk_col == indexed_col:
                return False

    return True


def _find_indexed_columns_for(index: exp.Index) -> list:
    idx_params = index.find(exp.IndexParameters)
    return [idx_params.args.get("columns")[i].name for i,x in enumerate(idx_params.args.get("columns"))]


def _find_referencing_columns_for(fk: exp.ForeignKey) -> list:
    expressions = fk.args.get("expressions")
    if expressions:
        names = []
        for expr in expressions:
            ident = expr if isinstance(expr, exp.Identifier) else expr.find(exp.Identifier)
            if ident:
                names.append(ident.name)
        return names

    # Fallback
    names = []
    for ident in fk.find_all(exp.Identifier):
        if ident.find_ancestor(exp.Reference) is None:
            names.append(ident.name)
    return names


def _find_table_for(node: exp.Expression) -> dict | None:
    # CREATE TABLE <tbl>(...)
    create = node.find_ancestor(exp.Create)
    if create:
        t = create.find(exp.Table)
        if t:
            return { "node": t,"name": t.this.sql(dialect=None) }

    # ALTER TABLE <tbl> ...
    alter = node.find_ancestor(exp.Alter)
    if alter:
        t = alter.find(exp.Table)
        if t:
            return { "node": t,"name": t.this.sql(dialect=None) }

    # CREATE INDEX ... ON <tbl> ...
    t = node.find(exp.Table)
    if t:
        return { "node": t,"name": t.this.sql(dialect=None) }

    return None
