from typing import Dict, List
from sqlglot import exp

from proton_pack.migration.rules.drop_columns import check_for_drop_columns
from proton_pack.migration.rules.foreign_key_without_supporting_indexes import check_for_foreign_key_without_supplementary_indexes
from proton_pack.migration.rules.non_concurrent_index_builds import has_non_concurrent_index_builds
from proton_pack.migration.rules.check_for_not_null_added_without_default import check_for_not_null_added_without_default


def analyze_ast(ast: List[exp.Expression]) -> Dict[str, List]:
    """
    Analyze a sqlglot AST for potentially dangerous operations.

    Current checks:
      - DROP_DETECTED: True if any DROP statement is present anywhere in the tree.
      - FOREIGN_KEY_WITHOUT_SUPP_INDEX: True if there is any foreign key without a supporting index.
      - NON_CONCURRENT_INDEX_BUILDS: True if there is any index, that is NOT concurrently built.
      - NOT_NULL_ADDED_WITHOUT_DEFAULT: True if there are ALTER TABLE operations adding NOT NULL without DEFAULT.
    """
    return {
        "DROP_DETECTED": check_for_drop_columns(ast),
        "FOREIGN_KEY_WITHOUT_SUPP_INDEX": check_for_foreign_key_without_supplementary_indexes(ast),
        "NON_CONCURRENT_INDEX_BUILDS": has_non_concurrent_index_builds(ast),
        "NOT_NULL_ADDED_WITHOUT_DEFAULT": check_for_not_null_added_without_default(ast),
    }
