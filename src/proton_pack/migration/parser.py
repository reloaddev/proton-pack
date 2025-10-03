from sqlglot import parse_one

def parse_sql_to_ast(sql):
    return parse_one(sql, dialect="postgres")