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
            Dropping tables or columns can permanently delete data. Before proceeding, verify that the data is either no
            longer needed or has been safely archived/backed up. In production, prefer a safe, multi-step approach:
              - Replace hard deletes with soft deletes when possible.
              - Migrate traffic away and remove application usage first.
              - Take a backup and validate restore procedures.
              - Drop objects only after verifying that no processes rely on them (including FKs/triggers).
        """), "  ")
        for operation in result.get("DROP_DETECTED"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  -- Check line {line.get_line_number()}: {line.line_content} \n"
        body += "\n"
    if any(result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX") or []):
        body += "🧩 [bold yellow]FOREIGN KEY[/] without index (slow queries)"
        body += textwrap.indent(textwrap.dedent("""
            Foreign keys should have a supporting index on the referencing column(s). Without it, Postgres may need to
            scan many rows to enforce FK checks on updates/deletes and to perform joins, leading to slow queries and
            increased locking.
            
            Note: Indexes add write overhead and storage. On highly insert-heavy tables that are rarely joined and where
            the referenced key is never updated/deleted, you might choose to omit the index—but this can make 
            updates/deletes of the referenced key and certain queries much slower.
            
            What to do:
              - Add an index on the foreign key column(s) of the referencing table.
              - For multi-column foreign keys, include all FK columns; keep their order as defined in the FK.
              - If queries also filter by other columns, consider a composite index with the FK columns first.
            Example: CREATE INDEX idx_<table>_<fk> ON <table>(<fk_column>);
            More info: https://stackoverflow.com/questions/970562/postgres-and-indexes-on-foreign-keys-and-primary-keys
                      https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK
        """), "  ")
        for operation in result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  -- Check line {line.get_line_number()}: {line.line_content} \n"
        body += "\n"
    if any(result.get("NON_CONCURRENT_INDEX_BUILDS") or []):
        body += "⏳ [bold yellow]INDEX[/] not built concurrently (table locks)"
        body += textwrap.indent(textwrap.dedent("""
            Prefer creating indexes CONCURRENTLY to avoid long exclusive locks on the table. On large tables, a
            non-concurrent build can block writes for a long time and impact availability.
            Recommended rollout:
              - Use: CREATE INDEX CONCURRENTLY idx_<table>_<col> ON <table>(<col>);
              - Run outside of a transaction block (Postgres requirement).
              - For existing duplicate/invalid indexes, drop them CONCURRENTLY as well.
            Docs: https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY
        """), "  ")
        for operation in result.get("NON_CONCURRENT_INDEX_BUILDS"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  -- Check line {line.get_line_number()}: {line.line_content} \n"
        body += "\n"
    if any(result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT") or []):
        body += "️🚨 [bold yellow]NOT NULL[/] added without DEFAULT (backfill risk)"
        body += textwrap.indent(textwrap.dedent("""
              Adding NOT NULL without a DEFAULT can fail if existing rows have NULLs and may require a table scan (locks/latency).
              What to do:
                - Backfill NULLs in batches.
                - (Optional) SET DEFAULT for future writes.
                - Add CHECK (col IS NOT NULL) NOT VALID; VALIDATE it; then ALTER COLUMN SET NOT NULL.
            Docs: https://www.postgresql.org/docs/current/sql-altertable.html
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
