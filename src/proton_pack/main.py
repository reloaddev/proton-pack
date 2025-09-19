import click
from sqlglot import parse_one

@click.group()
def cli():
    pass


@cli.command(name="parse")
@click.argument("sql")
def parse_sql_to_ast(sql):
    click.echo(f"\n\nSQL \n===\n {sql} \n\n")
    ast = repr(parse_one(sql))
    click.echo(f"AST \n===\n {ast} \n\n")