import sys
import click
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


@cli.command(name="check")
@click.argument("sql")
def check_migration(sql):
    ast = parse_sql_to_ast(sql)
    if "Drop" in ast:
        click.echo("DROP statement detected. Potential data loss!!!")
        sys.exit(1)
    click.echo("Migration check passed")
    sys.exit(0)

