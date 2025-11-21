import sys

from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.analyzer import analyze_ast
from proton_pack.pretty_printer import pretty_print

import os


def run():
    file_path = os.environ.get("MIGRATION_FILE")
    with open(file_path, "r") as f:
        sql = f.read()
    ast = parse_sql_to_ast(sql)
    result = analyze_ast(ast)

    printable_result = pretty_print(sql, result)

    # Write to output for further processing, currently unused
    output_path = os.environ.get("GITHUB_OUTPUT")
    with open(output_path, 'a') as f:
        f.write(f"analysis_result='{printable_result}'\n")

    if any(result.values()):
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__": # pragma: no cover
    run()