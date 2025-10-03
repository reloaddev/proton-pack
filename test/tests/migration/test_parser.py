import pytest
from proton_pack.migration.parser import parse_sql_to_ast


def test_parse_sql_to_ast():
    assert parse_sql_to_ast("SELECT * FROM ghosts").strip() == """
Select(
  expressions=[
    Star()],
  from=From(
    this=Table(
      this=Identifier(this=ghosts, quoted=False))))
   """.strip()
