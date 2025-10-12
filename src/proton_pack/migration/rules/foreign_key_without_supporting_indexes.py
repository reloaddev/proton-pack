from typing import List, Dict

from sqlglot import exp


def check_for_foreign_key_without_supplementary_indexes(ast: List[exp.Expression]) -> bool:
    """
    True iff there exists at least one table that defines a foreign key
    but has no indexes defined in the same migration AST.
    """
    per_table: Dict[str, Dict[str, bool]] = {}

    for tree in ast:
        for fk in tree.find_all(exp.ForeignKey):
            table_name = _find_table_for(fk)
            if table_name is None:
                continue
            per_table.setdefault(table_name, {"fk": False, "idx": False})
            per_table[table_name]["fk"] = True

        for idx in tree.find_all(exp.Index):
            table_name = _find_table_for(idx)
            if table_name is None:
                continue
            per_table.setdefault(table_name, {"fk": False, "idx": False})
            per_table[table_name]["idx"] = True

    return any(info["fk"] and not info["idx"] for info in per_table.values())


def _find_table_for(node: exp.Expression) -> str | None:
    # CREATE TABLE <tbl>(...)
    create = node.find_ancestor(exp.Create)
    if create:
        t = create.find(exp.Table)
        if t:
            return t.this.sql(dialect=None)

    # ALTER TABLE <tbl> ...
    alter = node.find_ancestor(exp.Alter)
    if alter:
        t = alter.find(exp.Table)
        if t:
            return t.this.sql(dialect=None)

    # CREATE INDEX ... ON <tbl> ...
    t = node.find(exp.Table)
    if t:
        return t.this.sql(dialect=None)

    return None