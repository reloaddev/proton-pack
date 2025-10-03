from proton_pack.migration.parser import parse_sql_to_ast
from sqlglot import exp


def test_parse_sql_to_ast():
    # given
    sql_string = "SELECT * FROM ghosts;"

    # when
    ast = parse_sql_to_ast(sql_string)

    # then
    assert ast.find(exp.Select) is not None
    assert ast.expressions[0].sql() == "*"
    assert ast.find(exp.Table).this.sql() == "ghosts"
