from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.rules.non_concurrent_index_builds import has_non_concurrent_index_builds

def test_non_concurrent_index_build():
    # given
    sql = """
        CREATE INDEX name_idx ON ghost(name);
    """

    # when
    ast = parse_sql_to_ast(sql)
    result = has_non_concurrent_index_builds(ast)

    # then
    assert result is True


def test_concurrent_index_build():
    # given
    sql = """
        CREATE INDEX name_idx CONCURRENTLY ON ghost(name);
    """

    # when
    ast = parse_sql_to_ast(sql)
    result = has_non_concurrent_index_builds(ast)

    # then
    assert result is False


def test_no_index_build():
    # given
    sql = "CREATE TABLE ghost;"

    # when
    ast = parse_sql_to_ast(sql)
    result = has_non_concurrent_index_builds(ast)

    # then
    assert result is False


def test_alter_index():
    # given
    sql = "ALTER INDEX name_idx ON ghost RENAME TO name_idx_new;"

    # when
    ast = parse_sql_to_ast(sql)
    result = has_non_concurrent_index_builds(ast)

    # then
    assert result is False


def test_drop_index():
    # given
    sql = "DROP INDEX name_idx;"

    # when
    ast = parse_sql_to_ast(sql)
    result = has_non_concurrent_index_builds(ast)

    # then
    assert result is False
