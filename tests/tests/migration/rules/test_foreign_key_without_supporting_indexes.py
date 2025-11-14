from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.rules.foreign_key_without_supporting_indexes import \
    check_for_foreign_key_without_supplementary_indexes


def test_adding_fk_index_on_table_creation():
    # given
    sql = """
        CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, reporter_id INTEGER, FOREIGN KEY (reporter_id) REFERENCES Human(id));
        CREATE INDEX ON ghost (reporter_id);
    """

    # when
    ast = parse_sql_to_ast(sql)
    result = check_for_foreign_key_without_supplementary_indexes(ast)

    # then
    assert result == []


def test_missing_fk_index_on_table_creation():
    # given
    sql = "CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, reporter_id INTEGER, FOREIGN KEY (reporter_id) REFERENCES Human(id));"

    # when
    ast = parse_sql_to_ast(sql)
    result = check_for_foreign_key_without_supplementary_indexes(ast)

    # then
    assert result == ast


# def test_fk_constraint_counter():
#     # given
#     sql = """
#         CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, reporter_id INTEGER);
#         ALTER TABLE ghost ADD CONSTRAINT fk_reporter FOREIGN KEY (reporter_id) REFERENCES human(id);
#         ALTER TABLE ghost DROP CONSTRAINT fk_reporter;
#     """
#
#     # when
#     ast = parse_sql_to_ast(sql)
#     result = check_for_foreign_key_without_supplementary_indexes(ast)
#
#     # then
#     assert result is True


# TODO Change implementation, so it can correctly detect when an fk index is dropped
# def test_removing_index_from_existing_fk():
#     # given
#     sql = """
#         CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, reporter_id INTEGER, FOREIGN KEY (reporter_id) REFERENCES human(id));
#         CREATE INDEX reporter_id_idx ON ghost (reporter_id);
#
#         -- Some other migrations
#
#         ALTER TABLE ghost DROP INDEX reporter_id_idx;
#     """
#
#     # when
#     ast = parse_sql_to_ast(sql)
#     result = check_for_foreign_key_without_supplementary_indexes(ast)
#
#     # then
#     assert result is False


def test_finding_foreign_key_constraint():
    # given
    sql = """
        CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, reporter_id INTEGER);
        ALTER TABLE ghost ADD CONSTRAINT fk_reporter FOREIGN KEY (reporter_id) REFERENCES human(id);
    """

    # when
    ast = parse_sql_to_ast(sql)
    result = check_for_foreign_key_without_supplementary_indexes(ast)

    # then
    assert result == [ast[1]]


def test_adding_fk_index_to_wrong_table():
    # given
    sql = """
        CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, reporter_id INTEGER, FOREIGN KEY (reporter_id) REFERENCES human(id));
        CREATE INDEX ON weapon (inventor_id);
    """

    # when
    ast = parse_sql_to_ast(sql)
    result = check_for_foreign_key_without_supplementary_indexes(ast)

    # then
    assert result == [ast[0]]


def test_drop_index_without_table():
    # given
    sql = "DROP INDEX name_idx;"

    # when
    ast = parse_sql_to_ast(sql)
    result = check_for_foreign_key_without_supplementary_indexes(ast)

    # then
    assert result == []


# def test_add_and_drop_index():
#     # given
#     sql = """
#         CREATE TABLE ghost (id INTEGER PRIMARY KEY, name TEXT, reporter_id INTEGER, FOREIGN KEY (reporter_id) REFERENCES Human(id));
#         CREATE INDEX name_idx ON ghost (reporter_id);
#         DROP INDEX name_idx;
#     """
#
#     # when
#     ast = parse_sql_to_ast(sql)
#     result = check_for_foreign_key_without_supplementary_indexes(ast)
#
#     # then
#     assert result is True



