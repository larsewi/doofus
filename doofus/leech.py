import os
import csv
from re import A
import re
from typing import Iterable
from doofus.block import Block

from doofus.utils import work_dir


def LCH_LoadTableCSV(path):
    if not os.path.isfile(path):
        return None
    with open(path, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    return rows


def LCH_StoreTableCSV(path, rows):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    return True


class LCH_Table:
    def __init__(
        self,
        primary: list,
        src: str,
        dest: str = None,
        load=LCH_LoadTableCSV,
        store=LCH_StoreTableCSV,
    ):
        self.primary = primary
        self.src = src
        self.dest = dest if dest else src
        self.load = load
        self.store = store


class LCH_Instance:
    def __init__(self, work_dir: str, tables: LCH_Table):
        if not os.path.isdir(work_dir):
            os.mkdir(work_dir)
        self.work_dir = work_dir
        self.tables = tables


def _rotate_fields(primary: str|tuple[str], table: list[list[str]]):
    """
    Rotate fields to have primary keys first, but keep the order within
    primary- and non-primary keys.
    """
    if isinstance(primary, str):
        primary = (primary,)

    fields = table[0]
    assert all(field in fields for field in primary), f"Primary keys {primary} not in fields {fields}"

    primary_indecies = [fields.index(f) for f in fields if f in primary]
    other_indecies = [fields.index(f) for f in fields if f not in primary]
    assert len(fields) == len(primary_indecies) + len(other_indecies)

    rotated = []
    for row in table:
        primary_cols = [row[i] for i in primary_indecies]
        other_cols = [row[i] for i in other_indecies]
        rotated.append(primary_cols + other_cols)
    return rotated


def _table_dict(primary: list[str], table: list[list[str]]):
    table = _rotate_fields(primary, table)
    fields = ",".join(table[0])
    rows = table[1:]

    dct = {}
    for row in rows:
        key = ",".join(row[:len(primary)])
        val = ",".join(row[len(primary):])
        dct[key] = val

    return fields, dct


def _calculate_table_diff(identifier, primary, new, old):
    primary_fields, other_fields, new = _table_dict(primary, new)
    _, _, old = _table_dict(primary, old)

    diff = [identifier, primary_fields, other_fields]
    insertions, deletions, modifications = 0, 0, 0

    # Rows added from new
    for key in new.keys() - old.keys():
        diff.append(f"+{key},{new[key]}")
        insertions += 1

    # Rows removed from new
    for key in old.keys() - new.keys():
        diff.append(f"-{key}")
        deletions += 1

    # Rows changed in new
    for key in new.keys() & old.keys():
        if new[key] != old[key]:
            diff.append(f"%{key},{new[key]}")
            modifications += 1

    return diff


def _get_head(workdir: str) -> str|None:
    path = os.path.join(work_dir, "HEAD")
    if os.path.isfile(path):
        with open(path, "r") as f:
            head = f.read(path)
        assert re.fullmatch(r"[0-9a-f]{40}", head), f"Bad hash from HEAD: {head}"
        return head
    return None


def commit(instance: LCH_Instance):
    new = {}
    for table in instance.tables:
        new[table.source] = (table.primary, table.load(table.source))

    head = _get_head(instance.work_dir)
    if head is None:
        # Iterate blocks to load old file
        assert False, "Not implemented"
    else:
        # Generate fake empty tables
        old = {key: (val[0], val[1][:1]) for key, val in new}

    assert dict(new.keys()) == dict(
        old.keys()
    ), f"Missmatching keys {dict(new.keys())} != {dict(old.keys())}"

    diffs = []
    for source in new.keys():
        diffs.append(source)
        primary, new_table = new[source]
        _, old_table = old[source]
        _calculate_table_diff(primary, new_table, old_table)
