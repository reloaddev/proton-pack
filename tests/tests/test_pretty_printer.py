from proton_pack.pretty_printer import pretty_print
from unittest.mock import patch

def test_similar_operation_lines():
    # given
    with patch("proton_pack.pretty_printer.parse_sql_line_to_ast") as mocked_parse:
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



