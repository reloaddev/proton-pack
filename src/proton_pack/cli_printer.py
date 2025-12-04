import textwrap
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .model.line import Line
from .migration.parser import parse_sql_line_to_ast

def pretty_print(sql, result) -> str:
    if not any(result.values()):
        return ""

    console = Console()
    text = Text("Migration Check Failed", style="bold red")
    body = "\n"
    if any(result.get("DROP_DETECTED") or []):
        body += "🔥 [bold yellow]DROP[/] statements detected (possible data loss)"
        body += textwrap.indent(textwrap.dedent("""
            Dropping tables and columns comes with the risk of data loss. You should make sure that the affected data is
            either irrelevant in future or properly backed up, before dropping any kind of data.
        """), "  ")
        for operation in result.get("DROP_DETECTED"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  -- Check line {line.get_line_number()}: {line.line_content} \n"
        body += "\n"
    if any(result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX") or []):
        body += "🧩 [bold yellow]FOREIGN KEY[/] without index (slow queries)"
        body += textwrap.indent(textwrap.dedent("""
            Creating an index on a foreign key can considerably increase query time. If multiple tables are queried
            together, it usually makes sense to create an index on foreign keys.
            See https://stackoverflow.com/questions/970562/postgres-and-indexes-on-foreign-keys-and-primary-keys
        """), "  ")
        for operation in result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  -- Check line {line.get_line_number()}: {line.line_content} \n"
        body += "\n"
    if any(result.get("NON_CONCURRENT_INDEX_BUILDS") or []):
        body += "⏳ [bold yellow]INDEX[/] not built concurrently (table locks)"
        body += textwrap.indent(textwrap.dedent("""
            Indexes should be created concurrently, to avoid locking of tables in PostgresDB. Imagine you have a large
            table with a lot of data. Creating an index on of the columns means that the DBMS has to traverse every row,
            which can potentially take a long time. For that time the affected table is unavailable for writes, which
            can impact the availability of production systems. Building indexes concurrently avoids that problem.
            See https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY
        """), "  ")
        for operation in result.get("NON_CONCURRENT_INDEX_BUILDS"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  -- Check line {line.get_line_number()}: {line.line_content} \n"
        body += "\n"
    if any(result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT") or []):
        body += "🚨 [bold yellow]NOT NULL[/] added without DEFAULT (backfill risk)"
        body += textwrap.indent(textwrap.dedent("""
            Changing a column to be NOT NULL, with existing rows containing NULL values, leads to errors in Postgres, if 
            no new default value is provided. This can potentially break production deployments, if not fixed in time.
            See https://stackoverflow.com/questions/3997966/can-i-add-a-not-null-column-without-default-value
        """), "  ")
        for operation in result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  -- Check line {line.get_line_number()}: {line.line_content} \n"
        body += "\n"

    console.print(Panel(body, title=text))
    return body


def _find_failing_line(sql, operation) -> Line | None:
    lines_of_sql = sql.split("\n")
    for index, line in enumerate(lines_of_sql):
        line = line.strip()
        if line is None or line == "":
            continue
        parsed = parse_sql_line_to_ast(line)
        if parsed == operation:
            return Line(index, line)
    return None
