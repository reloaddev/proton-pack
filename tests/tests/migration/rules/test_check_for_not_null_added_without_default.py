from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.rules.check_for_not_null_added_without_default import (
    check_for_not_null_added_without_default,
)


def test_detects_set_not_null_without_default():
    sql = "ALTER TABLE users ALTER COLUMN name SET NOT NULL;"
    ast = parse_sql_to_ast(sql)
    assert check_for_not_null_added_without_default(ast) is True


def test_ignores_set_not_null_when_default_provided_in_same_statement():
    sql = """
    ALTER TABLE users
      ALTER COLUMN name SET DEFAULT 'unknown',
      ALTER COLUMN name SET NOT NULL;
    """
    ast = parse_sql_to_ast(sql)
    assert check_for_not_null_added_without_default(ast) is False


def test_detects_add_column_not_null_without_default():
    sql = "ALTER TABLE users ADD COLUMN classification TEXT NOT NULL;"
    ast = parse_sql_to_ast(sql)
    assert check_for_not_null_added_without_default(ast) is False


def test_ignores_add_column_not_null_with_default():
    sql = "ALTER TABLE users ADD COLUMN classification TEXT NOT NULL DEFAULT 'foo';"
    ast = parse_sql_to_ast(sql)
    assert check_for_not_null_added_without_default(ast) is False