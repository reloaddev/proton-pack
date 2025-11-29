from proton_pack.cli_printer import pretty_print
from unittest.mock import patch

from proton_pack.model.line import Line


def test_similar_operation_lines():
    # given
    with patch("proton_pack.cli_printer.parse_sql_line_to_ast") as mocked_parse:
        # given
        sql = """
            ALTER TABLE ghost DROP COLUMN name;
            ALTER TABLE ghost DROP COLUMN type;
        """
        result = {
            "DROP_DETECTED": ["DROP_COL_NAME", "DROP_COL_TYPE"]
        }
        # due to _find_failing_line always traversing the whole SQL,
        # parse_sql_line_to_ast is called 3 times in this case
        mocked_parse.side_effect = [
            "DROP_COL_NAME", # _find_failing_line(sql, "DROP_COL_NAME") <-- match
            "DROP_COL_NAME", # _find_failing_line(sql, "DROP_COL_TYPE")
            "DROP_COL_TYPE" # _find_failing_line(sql, "DROP_COL_TYPE") <-- match
        ]

        # when
        print_result = pretty_print(sql, result)

        # then
        mocked_parse.assert_called()
        mocked_parse.call_count = 2
        assert "- Check line 1: ALTER TABLE ghost DROP COLUMN name;" in print_result
        assert "- Check line 2: ALTER TABLE ghost DROP COLUMN type;" in print_result


def test_cli_printer_returns_empty_when_no_issues():
    # given
    sql = """
        -- harmless migration with no changes
    """
    result = {}

    # when
    out = pretty_print(sql, result)

    # then
    assert out == ""


def test_cli_printer_renders_each_section_with_lines():
    # given
    sql = """
        ALTER TABLE t DROP COLUMN c1;
        ALTER TABLE t ADD CONSTRAINT fk FOREIGN KEY (c) REFERENCES p(id);
        CREATE INDEX idx ON t(c);
        ALTER TABLE t ALTER COLUMN c SET NOT NULL;
    """
    result = {
        "DROP_DETECTED": ["DROP_OP"],
        "FOREIGN_KEY_WITHOUT_SUPP_INDEX": ["FK_NO_IDX"],
        "NON_CONCURRENT_INDEX_BUILDS": ["IDX_NON_CONCURRENT"],
        "NOT_NULL_ADDED_WITHOUT_DEFAULT": ["NN_NO_DEFAULT"],
    }

    # Patch _find_failing_line to avoid complex parser side effects and focus on rendering
    with patch("proton_pack.cli_printer._find_failing_line") as find_line:
        find_line.side_effect = [
            Line(0, "ALTER TABLE t DROP COLUMN c1;"),
            Line(1, "ALTER TABLE t ADD CONSTRAINT fk FOREIGN KEY (c) REFERENCES p(id);"),
            Line(2, "CREATE INDEX idx ON t(c);"),
            Line(3, "ALTER TABLE t ALTER COLUMN c SET NOT NULL;"),
        ]

        # when
        out = pretty_print(sql, result)

    # then: section headers (Rich markup) are present
    assert "🔥 [bold yellow]DROP[/] statements detected (possible data loss)" in out
    assert "🧩 [bold yellow]FOREIGN KEY[/] without index (slow queries)" in out
    assert "⏳ [bold yellow]INDEX[/] not built concurrently (table locks)" in out
    assert "⚠️  [bold yellow]NOT NULL[/] added without DEFAULT (backfill risk)" in out

    # and each bullet line exists with correct content
    assert "- Check line 0: ALTER TABLE t DROP COLUMN c1;" in out
    assert (
        "- Check line 1: ALTER TABLE t ADD CONSTRAINT fk FOREIGN KEY (c) REFERENCES p(id);"
        in out
    )
    assert "- Check line 2: CREATE INDEX idx ON t(c);" in out
    assert "- Check line 3: ALTER TABLE t ALTER COLUMN c SET NOT NULL;" in out


def test_cli_printer_skips_bullet_when_no_line_found():
    # given
    sql = """
        ALTER TABLE t DROP COLUMN c1;
    """
    result = {"DROP_DETECTED": ["DROP_OP"]}

    with patch("proton_pack.cli_printer._find_failing_line", return_value=None):
        # when
        out = pretty_print(sql, result)

    # then: header printed but no bullet line added
    assert "DROP[/] statements detected" in out
    assert "- Check line" not in out

