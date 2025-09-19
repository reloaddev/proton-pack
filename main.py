from sqlglot import parse_one

print(repr(parse_one("SELECT a + 1 AS z")))