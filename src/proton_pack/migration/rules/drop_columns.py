from sqlglot import exp

def check_for_drop_columns(ast: exp.Expression) -> bool:
    is_dropping_columns = ast.find(exp.Drop) is not None
    return is_dropping_columns