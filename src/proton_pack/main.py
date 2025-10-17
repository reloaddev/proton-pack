import sys
import click

from .migration.analyzer import analyze_ast
from .migration.parser import parse_sql_to_ast
from .pretty_printer import pretty_print


@click.group()
def cli():
    pass


@cli.command(name="parse")
@click.argument("file_path")
def parse(file_path):
    with open(file_path, "r") as f:
        sql = f.read()
    click.echo(f"\n\nSQL \n===\n {sql} \n\n")
    ast = parse_sql_to_ast(sql)
    click.echo(f"AST \n===\n {ast} \n\n")


@cli.command(name="analyze")
@click.argument("file_path")
def analyze(file_path):
    with open(file_path, "r") as f:
        sql = f.read()
    ast = parse_sql_to_ast(sql)
    result = analyze_ast(ast)
    pretty_print(result)

    if any(result):
        sys.exit(1)

    click.echo("Migration check passed.")
    sys.exit(0)
