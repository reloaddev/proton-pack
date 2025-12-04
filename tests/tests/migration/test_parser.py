from proton_pack.migration.parser import parse_sql_to_ast
from sqlglot import exp


def test_ignore_alembic_related_statements():
    # given
    sql = """
        CREATE TABLE alembic_version (
            version_num VARCHAR(32) NOT NULL, 
            CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
        );
        SELECT * FROM ghosts;
        INSERT INTO alembic_version (version_num) VALUES ('33018f72f5b1') RETURNING alembic_version.version_num;
    """

    # when
    ast = parse_sql_to_ast(sql)

    # then
    assert len(ast) != 3 # 2 Alembic related statements
    assert len(ast) == 1
    assert isinstance(ast[0], exp.Select)
