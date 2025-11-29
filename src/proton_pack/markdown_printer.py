from .model.line import Line
from .migration.parser import parse_sql_line_to_ast


def pretty_print(sql: str, result) -> str:
    """
    Produce a Markdown formatted report for GitHub comments based on the
    analysis result. Returns an empty string when there are no issues.
    """
    if not any(result.values()):
        return ""

    parts: list[str] = ["### Migration Check Failed\n"]

    # DROP statements
    if any(result.get("DROP_DETECTED") or []):
        parts.append("- 🔥 **DROP** statements detected (possible data loss)")
        for operation in result.get("DROP_DETECTED"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: `{line.line_content}`"
                )

    # FOREIGN KEY without supporting index
    if any(result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX") or []):
        parts.append("- 🧩 **FOREIGN KEY** without index (slow queries)")
        for operation in result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: `{line.line_content}`"
                )

    # Non-concurrent index builds
    if any(result.get("NON_CONCURRENT_INDEX_BUILDS") or []):
        parts.append("- ⏳ **INDEX** not built concurrently (table locks)")
        for operation in result.get("NON_CONCURRENT_INDEX_BUILDS"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: `{line.line_content}`"
                )

    # NOT NULL added without DEFAULT
    if any(result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT") or []):
        parts.append("- ⚠️  **NOT NULL** added without DEFAULT (backfill risk)")
        for operation in result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: `{line.line_content}`"
                )

    return "\n".join(parts) + "\n"


def _find_failing_line(sql: str, operation) -> Line | None:
    lines_of_sql = sql.split("\n")
    for index, line in enumerate(lines_of_sql):
        line = line.strip()
        if line is None or line == "":
            continue
        parsed = parse_sql_line_to_ast(line)
        if parsed == operation:
            return Line(index, line)
    return None
