from .model.line import Line
from .migration.parser import parse_sql_line_to_ast


def _md_escape(text: str) -> str:
    """Escape Markdown-sensitive underscores to render them literally."""
    if text is None:
        return ""
    return text.replace("_", "\\_")


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
        parts.append("🔥 **DROP** statements detected (possible data loss)")
        parts.append(
            "  Dropping tables or columns can permanently delete data. Before proceeding, verify that the data is either no\n"
            "  longer needed or has been safely archived/backed up. In production, prefer a safe, multi-step approach:"
        )
        parts.extend(
            [
                "  - Replace hard deletes with soft deletes when possible.",
                "  - Migrate traffic away and remove application usage first.",
                "  - Take a backup and validate restore procedures.",
                "  - Drop objects only after verifying that no processes rely on them (including FKs/triggers).",
            ]
        )
        for operation in result.get("DROP_DETECTED"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: {_md_escape(line.line_content)}"
                )
        parts.append("")

    # FOREIGN KEY without supporting index
    if any(result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX") or []):
        parts.append("🧩 **FOREIGN KEY** without index (slow queries)")
        parts.append(
            "  Foreign keys should have a supporting index on the referencing column(s). Without it, Postgres may need to\n"
            "  scan many rows to enforce FK checks on updates/deletes and to perform joins, leading to slow queries and\n"
            "  increased locking.\n\n"
            "  Note: Indexes add write overhead and storage. On highly insert-heavy tables that are rarely joined and where\n"
            "  the referenced key is never updated/deleted, you might choose to omit the index—but this can make\n"
            "  updates/deletes of the referenced key and certain queries much slower.\n\n"
            "  What to do:"
        )
        parts.extend(
            [
                "  - Add an index on the foreign key column(s) of the referencing table.",
                "  - For multi-column foreign keys, include all FK columns; keep their order as defined in the FK.",
                "  - If queries also filter by other columns, consider a composite index with the FK columns first.",
                "  - More info: https://stackoverflow.com/questions/970562/postgres-and-indexes-on-foreign-keys-and-primary-keys",
                "              https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK",
            ]
        )
        for operation in result.get("FOREIGN_KEY_WITHOUT_SUPP_INDEX"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: {_md_escape(line.line_content)}"
                )
        parts.append("")

    # Non-concurrent index builds
    if any(result.get("NON_CONCURRENT_INDEX_BUILDS") or []):
        parts.append("⏳ **INDEX** not built concurrently (table locks)")
        parts.append(
            "  Prefer creating indexes CONCURRENTLY to avoid long exclusive locks on the table. On large tables, a\n"
            "  non-concurrent build can block writes for a long time and impact availability.\n"
            "  Recommended rollout:"
        )
        parts.extend(
            [
                "  - Run outside of a transaction block (Postgres requirement).",
                "  - For existing duplicate/invalid indexes, drop them CONCURRENTLY as well.",
                "  - Docs: https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY",
            ]
        )
        for operation in result.get("NON_CONCURRENT_INDEX_BUILDS"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: {_md_escape(line.line_content)}"
                )
        parts.append("")

    # NOT NULL added without DEFAULT
    if any(result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT") or []):
        parts.append("🚨 **NOT NULL** added without DEFAULT (backfill risk)")
        parts.append(
            "  Adding NOT NULL without a DEFAULT can fail if existing rows have NULLs and may require a table scan (locks/latency).\n"
            "  What to do:"
        )
        parts.extend(
            [
                "  - Backfill NULLs in batches.",
                "  - (Optional) SET DEFAULT for future writes.",
                "  - Add CHECK (col IS NOT NULL) NOT VALID; VALIDATE it; then ALTER COLUMN SET NOT NULL.",
                "  - Docs: https://www.postgresql.org/docs/current/sql-altertable.html",
            ]
        )
        for operation in result.get("NOT_NULL_ADDED_WITHOUT_DEFAULT"):
            line = _find_failing_line(sql, operation)
            if line is not None and line != "":
                parts.append(
                    f"  - Check line {line.get_line_number()}: {_md_escape(line.line_content)}"
                )
        parts.append("")

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
