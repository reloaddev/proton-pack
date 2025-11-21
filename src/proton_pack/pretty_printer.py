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
        body += "🔥 [bold yellow]DROP[/] statements detected (possible data loss)\n"
        for operation in result.get("DROP_DETECTED"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  - Check line {line.get_line_number()}: {line.line_content} \n"
    if any(result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX") or []):
        body += "🧩 [bold yellow]FOREIGN KEY[/] without index (slow queries)\n"
        for operation in result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  - Check line {line.get_line_number()}: {line.line_content} \n"
    if any(result.get("NON_CONCURRENT_INDEX_BUILDS") or []):
        body += "⏳ [bold yellow]INDEX[/] not built concurrently (table locks)\n"
        for operation in result.get("NON_CONCURRENT_INDEX_BUILDS"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  - Check line {line.get_line_number()}: {line.line_content} \n"
    if any(result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT") or []):
        body += "⚠️  [bold yellow]NOT NULL[/] added without DEFAULT (backfill risk)\n"
        for operation in result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                body += f"  - Check line {line.get_line_number()}: {line.line_content} \n"

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
