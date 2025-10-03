from sqlglot import parse_one

def parse_sql_to_ast(sql):
    return repr(parse_one(sql))