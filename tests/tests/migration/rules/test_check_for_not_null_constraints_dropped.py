from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.rules.check_for_not_null_constraints_dropped import (
    check_for_not_null_constraints_dropped,
)


def test_detects_drop_not_null_simple():
    sql = "ALTER TABLE users ALTER COLUMN name DROP NOT NULL;"
    ast = parse_sql_to_ast(sql)
    assert check_for_not_null_constraints_dropped(ast) is True


def test_ignores_set_not_null():
    sql = "ALTER TABLE users ALTER COLUMN name SET NOT NULL;"
    ast = parse_sql_to_ast(sql)
    assert check_for_not_null_constraints_dropped(ast) is False