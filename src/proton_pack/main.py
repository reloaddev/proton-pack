import os
import sys
import click

from .migration.analyzer import analyze_ast
from .migration.parser import parse_sql_to_ast
from .pretty_printer import pretty_print


@click.group()
def cli():
    pass


@cli.command(name="parse")
@click.argument("path")
def parse(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            sql = f.read()
    elif os.path.isdir(path):
        sql = _read_migration_directory(path)
    else:
        click.echo("No migration files found.")


    click.echo(f"\n\nSQL \n===\n {sql} \n\n")
    ast = parse_sql_to_ast(sql)
    click.echo(f"AST \n===\n {ast} \n\n")


@cli.command(name="analyze")
@click.argument("path")
def analyze(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            sql = f.read()
    elif os.path.isdir(path):
        sql = _read_migration_directory(path)
    else:
        click.echo("No migration files found.")

    ast = parse_sql_to_ast(sql)
    result = analyze_ast(ast)
    pretty_print(result)

    if any(result):
        sys.exit(1)

    click.echo("Migration check passed.")
    sys.exit(0)


def _read_migration_directory(directory_path) -> str | None:
    directory = os.fsencode(directory_path)
    if directory is None:
        return None

    read_content = ""

    files = os.listdir(directory)
    sorted_files = sorted(files, key=lambda  f: os.path.getmtime(f"{directory_path}/{os.fsdecode(f)}"), reverse=False)

    for file in sorted_files:
        filename = os.fsdecode(file)
        filename_path = f"{directory_path}/{filename}"
        if os.path.isdir(filename_path):
            continue

        if filename.endswith(".sql"):
            with open(filename_path, "r") as opened_file:
                read_content += "\n\n"
                read_content += opened_file.read()

    return read_content