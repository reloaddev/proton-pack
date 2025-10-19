import sys

from proton_pack.migration.parser import parse_sql_to_ast
from proton_pack.migration.analyzer import analyze_ast

import os

file_path = os.environ.get("MIGRATION_FILE")
with open(file_path, "r") as f:
    sql = f.read()
ast = parse_sql_to_ast(sql)
result = analyze_ast(ast)

output_path = os.environ.get('GITHUB_OUTPUT')
with open(output_path, 'a') as f:
    f.write(f'analysis_result={result}\n')

if any(result):
    sys.exit(1)
sys.exit(0)