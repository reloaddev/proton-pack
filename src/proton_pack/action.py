import sys

from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.analyzer import analyze_ast

import os

file_path = os.environ.get("MIGRATION_FILE")
with open(file_path, "r") as f:
    sql = f.read()
ast = parse_sql_to_ast(sql)
result = analyze_ast(ast)

print(f"::set-output name=analysis_result::{result}")

if any(result):
    sys.exit(1)
sys.exit(0)