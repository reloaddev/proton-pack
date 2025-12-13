import sqlglot
from sqlglot import exp
from typing import List, Dict, Any, Tuple, Optional

# --- MOCK SCHEMA (Simulates looking up the OLD type in the database) ---
# When analyzing an ALTER TABLE statement, we only see the *new* type.
# We need the existing type to determine if the change is narrowing.
MOCK_SCHEMA: Dict[str, Dict[str, str]] = {
    "humans": {
        "id": "INT",
        "name": "Text",
        "email": "Text",
        "hire_date": "Date"
    },
    "ghost": {
        "id": "INT",
        "name": "Text",
        "spooky_level": "INT",
        "ectoplasm_volume": "BIGINT",
        "reporter_id": "BIGINT",
        "danger_rating": "INT"
    }
}

# --- Sample SQL Statement (String Input) ---
# This string will be parsed into the AST before being passed to the analyzer function.
SAMPLE_SQL_INPUT = """
ALTER TABLE finance_data
    ALTER COLUMN price TYPE DECIMAL(8, 2), -- Narrowing (10, 5) -> (8, 2)
    ALTER COLUMN exchange_rate TYPE DECIMAL(15, 10); -- Widening (DOUBLE -> DECIMAL) - Can be complex, but not numeric narrowing
    
ALTER TABLE products
    ALTER COLUMN description TYPE VARCHAR(200); -- Narrowing (500 -> 200)

ALTER TABLE user_metrics
    ALTER COLUMN event_count TYPE INT; -- Narrowing (BIGINT -> INT)
    
ALTER TABLE inventory
    ALTER COLUMN cost TYPE NUMERIC(15, 5); -- Narrowing (15, 8) -> (15, 5)
"""


def get_type(type_str: str) -> Dict[str, Any]:
    # Getting info from pertaining to INT(s) and VARCHAR(s)
    # type, length(max number of characters), precision(total number of characters) and scale(only for DECIMAL, numbers after decimal point.)
    info = {'type': type_str.upper(), 'length': None, 'precision': None, 'scale': None}
    
    try:
        type_exp = exp.DataType.build(type_str)
    except Exception:
        return info

    # Extract length(for VARCHAR, CHAR)
    if type_exp.this.is_string:
        length_exp = type_exp.args.get('length')
        if length_exp and isinstance(length_exp, exp.Literal):
            info['length'] = int(length_exp.this)
            
    # Extract Precision and Scale(for DECIMAL, NUMERIC)
    if type_exp.this.is_decimal:
        precision_exp = type_exp.args.get('precision')
        scale_exp = type_exp.args.get('scale')
        
        if precision_exp and isinstance(precision_exp, exp.Literal):
            info['precision'] = int(precision_exp.this)
            
        if scale_exp and isinstance(scale_exp, exp.Literal):
            info['scale'] = int(scale_exp.this)

    return info

def check_varchar_narrowing(old_info: Dict, new_info: Dict) -> Tuple[bool, str]:
    # Check that both are fixed-length string types
    if not (old_info.get('length') is not None and new_info.get('length') is not None):
        return False, ""
        
    old_length = old_info['length']
    new_length = new_info['length']
    
    if new_length < old_length:
        message = f"Length reduced from {old_length} to {new_length}."
        return True, message

    return False, ""

def check_decimal_narrowing(old_info: Dict, new_info: Dict) -> Tuple[bool, str]:
    """
    Checks for DECIMAL/NUMERIC precision or scale reduction (Narrowing).
    """
    old_prec = old_info.get('precision')
    new_prec = new_info.get('precision')
    old_scale = old_info.get('scale')
    new_scale = new_info.get('scale')
    
    if old_prec is None or new_prec is None:
        return False, ""
        
    messages = []

    # Total Precision Narrowing (loss of magnitude)
    if new_prec < old_prec:
        messages.append(f"Total precision reduced from {old_prec} to {new_prec}.")

    # Scale Narrowing (loss of decimal precision)
    if old_scale is not None and new_scale is not None and new_scale < old_scale:
        messages.append(f"Decimal scale (digits after decimal) reduced from {old_scale} to {new_scale}.")

    if messages:
        return True, " | ".join(messages)
    
    return False, ""


def check_bigint_to_int(old_type: str, new_type: str) -> Tuple[bool, str]:
    """
    Checks for BIGINT to INT or other related size-class narrowing (string comparison).
    """
    # Changes types to uppercase and strip non-alphanumeric for checking
    old_norm = old_type.upper().split('(')[0].strip()
    new_norm = new_type.upper().split('(')[0].strip()

    big_to_int_map = {
        'BIGINT': ['INT', 'MEDIUMINT', 'SMALLINT', 'TINYINT'],
        'INT': ['MEDIUMINT', 'SMALLINT', 'TINYINT'],
        'MEDIUMINT': ['SMALLINT', 'TINYINT'],
        'SMALLINT': ['TINYINT']
    }

    if old_norm in big_to_int_map and new_norm in big_to_int_map.get(old_norm, []):
        # Maximum value for a signed 32-bit INT
        int_max = 2**31 - 1
        message = (
            f"Size class reduced from {old_norm} to {new_norm}. "
            f"Existing values may exceed the new type's max limit (~ {int_max:,} for normal INT)."
        )
        return True, message

    return False, ""


def analyze_narrowing_changes(ast_expressions: List[exp.Expression]):
    narrowing_changes = []
    
    # The input is now assumed to be a list of AST expressions
    for ast in ast_expressions:
        # Check if the expression is an ALTER TABLE statement
        if isinstance(ast, exp.Alter):
            table_name = ast.this.name
            
            # Iterate through the alterations (ADD, DROP, ALTER COLUMN)
            for action in ast.args.get('actions', []):
                is_type_change_action = (
                    isinstance(action, exp.AlterColumn) and action.args.get('this') == exp.Set
                ) or isinstance(action, exp.ChangeColumn)
                
                if is_type_change_action:
                    
                    column_name = action.this.name
                    # 'to' holds the new type for SET DATA TYPE or similar operations
                    new_type_exp = action.args.get('to') 
                    
                    if not new_type_exp or not isinstance(new_type_exp, exp.DataType):
                        continue # Not a type change operation

                    # 1. Get the NEW type string from the AST expression
                    new_type_str = new_type_exp.sql()
                    
                    # 2. Getting the OLD type from mock schema, should be changed to the snapshot when implemented
                    old_type_str = ast_expressions.get(table_name, {}).get(column_name)

                    if not old_type_str:
                        print(f"skipping {table_name}.{column_name}: Old type not found in schema. Skipping analysis.")
                        continue
                        
                    is_narrowing = False
                    reason = ""
                    
                    old_info = get_type(old_type_str)
                    new_info = get_type(new_type_str)
                    
                    
                    # Check for VARCHAR/CHAR length reduction
                    if not is_narrowing:
                        is_narrowing, reason = check_varchar_narrowing(old_info, new_info)
                    
                    # Check for DECIMAL/NUMERIC precision/scale reduction
                    if not is_narrowing and ('DECIMAL' in old_info['type'] or 'NUMERIC' in old_info['type']):
                        is_narrowing, reason = check_decimal_narrowing(old_info, new_info)
                        
                    # Check for BIGINT/INT size class reduction
                    if not is_narrowing:
                        is_narrowing, reason = check_bigint_to_int(old_type_str, new_type_str)

                    # Report
                    print(f"[STATUS] {table_name}.{column_name}: {old_type_str} -> {new_type_str} {'(⚠️ NARROWING)' if is_narrowing else '(✅ SAFE)'}")

                    if is_narrowing:
                        narrowing_changes.append({
                            'table': table_name,
                            'column': column_name,
                            'old': old_type_str,
                            'new': new_type_str,
                            'reason': reason
                        })
                        
    print("\n" + "="*70)
    print(f"REPORT: Found {len(narrowing_changes)} Critical Narrowing Change(s)")
    print("="*70)
    
    if narrowing_changes:
        for nc in narrowing_changes:
            print(f"⚠️ {nc['table']}.{nc['column']}")
            print(f"  Type Change: {nc['old']} -> {nc['new']}")
            print(f"  Reason: {nc['reason']}\n")
    else:
        print("No critical narrowing changes detected for the monitored types.")