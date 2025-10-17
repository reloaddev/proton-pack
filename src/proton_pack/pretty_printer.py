from typing import Dict


def pretty_print(result: Dict[str, bool]):
    if not any(result):
        return

    print('\n')

    print("!! Migration Check Failed !!")
    if result["DROP_DETECTED"]:
        print(" - DROP statements detected. This can lead to data loss.")
    if result["FOREIGN_KEY_WITHOUT_SUPP_INDEX"]:
        print(" - FOREIGN KEY without supplementary index detected. This can result in suboptimal query performance.")
    if result["NON_CONCURRENT_INDEX_BUILDS"]:
        print(" - INDEX detected, that is not concurrently built. This can lead to locked database tables.")

    print('\n')