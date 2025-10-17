from typing import List

from sqlglot import exp, parse


def parse_sql_to_ast(sql) -> List[exp.Expression]:
    parsed = parse(sql, dialect="postgres")
    return [p for p in parsed if p is not None]
