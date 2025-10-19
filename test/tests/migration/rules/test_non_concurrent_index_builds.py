from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.rules.non_concurrent_index_builds import has_non_concurrent_index_builds

def test_check_failing_for_non_concurrent_index_build():
    # given
    sql = """
        CREATE INDEX ON ghosts;
    """

    # when
    ast = parse_sql_to_ast(sql)
    result = has_non_concurrent_index_builds(ast)

    # then
    assert result is True

def test_check_passing_for_non_concurrent_index_build():
    # given
    sql = """
        CREATE INDEX CONCURRENTLY ON ghosts;
    """

    # when
    ast = parse_sql_to_ast(sql)
    result = has_non_concurrent_index_builds(ast)

    # then
    assert result is False