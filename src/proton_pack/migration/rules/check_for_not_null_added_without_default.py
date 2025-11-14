from typing import List
from sqlglot import exp


def check_for_not_null_added_without_default(ast: List[exp.Expression]) -> List[exp.Expression]:
    """
    Detect ALTER TABLE operations that add NOT NULL to an existing column without providing a DEFAULT.

    Risky pattern:
      - ALTER TABLE ... ALTER COLUMN ... SET NOT NULL (without a SET DEFAULT anywhere in the statement)

    Note: ADD COLUMN ... NOT NULL is allowed (safe at creation time), so it's ignored.
    """
    unsafe = []
    for tree in ast:
        set_not_null = False
        set_default = False
        alter = tree.find(exp.Alter)
        if alter:
            # SET NOT NULL can be rendered as AlterColumn, if standalone
            for alter_column in (alter.find_all(exp.AlterColumn) or []):
                if not alter_column.args.get("allow_null"):
                    set_not_null = True

            # This part could be interesting when considering schema state
            # SET NOT NULL can be rendered as ColumnConstraint, if in one line with DEFAULT
            # for column_constraint in (alter.find_all(exp.ColumnConstraint) or []):
            #     print(type(column_constraint.kind))
            #     if column_constraint.kind and type(column_constraint.kind) is exp.NotNullColumnConstraint:
            #         set_not_null = True
            #     elif column_constraint.kind and type(column_constraint.kind) is exp.DefaultColumnConstraint:
            #         set_default = True

        # In sqlglot the DEFAULT expression is rendered as a COMMAND instead of ALTER
        # In combined statements ('NOT NULL' + 'DEFAULT' as separate ALTER COLUMN) both are rendered as expressions of a COMMAND
        command = tree.find(exp.Command)
        if command and command.this == "ALTER" and command.expression:

            if "ALTER COLUMN".lower() in command.expression.lower() and "SET NOT NULL".lower() in command.expression.lower():
                set_not_null = True
            if "ALTER COLUMN".lower() in command.expression.lower() and "DEFAULT".lower() in command.expression.lower():
                set_default = True

        if set_not_null and not set_default:
            unsafe.append(alter if alter else command)

    return unsafe