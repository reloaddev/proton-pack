from typing import List
from sqlglot import exp


def has_non_concurrent_index_builds(ast: List[exp.Expression]):
    """
        A standard index build (without CONCURRENTLY) locks out writes (but not reads) on the table until it's done.
        This can impact the availability of tables negatively.
    """
    unsafe = []

    for tree in ast:
        indexes = tree.find_all(exp.Index)
        for index in indexes:
            create = index.find_ancestor(exp.Create)
            if create.args.get("kind") == "INDEX":
                if create.args.get("concurrently") is None:
                    unsafe.append(index)

    return True if any(unsafe) else False