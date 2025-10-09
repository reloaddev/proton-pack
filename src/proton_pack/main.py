import sys
import click

from .migration.analyzer import analyze_ast
from .migration.parser import parse_sql_to_ast

@click.group()
def cli():
    pass


@cli.command(name="debug")
@click.argument("sql")
def debug(sql):
    click.echo(f"\n\nSQL \n===\n {sql} \n\n")
    ast = parse_sql_to_ast(sql)
    click.echo(f"AST \n===\n {ast} \n\n")


@cli.command(name="analyze")
@click.argument("sql")
def analyze_migration(sql):
    ast = parse_sql_to_ast(sql)
    result = analyze_ast(ast)
    if result["DROP_DETECTED"]:
        click.echo("Migration check failed! DROP statements detected.")
        sys.exit(1)
    if result["FOREIGN_KEY_WITHOUT_SUPP_INDEX"]:
        click.echo("Migration check failed! Foreign key without supplementary index detected.")
        sys.exit(1)
    click.echo("Migration check passed.")
    sys.exit(0)


@cli.command(name="analyze-file")
@click.argument("file_path")
def analyze_migration_file(file_path):
    with open(file_path, "r") as f:
        sql = f.read()
    ast = parse_sql_to_ast(sql)
    result = analyze_ast(ast)
    if result["DROP_DETECTED"]:
        click.echo("Migration check failed! DROP statements detected.")
        sys.exit(1)
    if result["FOREIGN_KEY_WITHOUT_SUPP_INDEX"]:
        click.echo("Migration check failed! Foreign key without supplementary index detected.")
        sys.exit(1)
    click.echo("Migration check passed.")
    sys.exit(0)
