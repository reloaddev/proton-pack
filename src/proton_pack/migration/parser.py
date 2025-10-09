from typing import List

from sqlglot import exp, parse


def parse_sql_to_ast(sql) -> List[exp.Expression]:
    return parse(sql, dialect="postgres")
