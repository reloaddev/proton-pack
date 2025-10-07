from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.analyzer import analyze_ast  # to be implemented


def test_drop_statement_is_flagged():
    # given
    sql = "DROP TABLE ghosts;"

    # when
    ast = parse_sql_to_ast(sql)
    result = analyze_ast(ast)

    # then
    assert isinstance(result, dict)
    assert result.get("DROP_DETECTED") is True
