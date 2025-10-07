from proton_pack.migration.parser import parse_sql_to_ast
from sqlglot import exp


def test_parse_sql_to_ast():
    # given
    sql = "SELECT * FROM ghosts;"

    # when
    ast = parse_sql_to_ast(sql)

    # then
    assert isinstance(ast, exp.Select)

    table = ast.args["from"].this
    assert isinstance(table, exp.Table)
    assert table.name == "ghosts"

    assert any(isinstance(e, exp.Star) for e in ast.expressions)
