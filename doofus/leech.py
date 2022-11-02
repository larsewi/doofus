import os
import csv
import re
import datetime
import logging as log
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


def _rotate_fields(primary, table: list[list[str]]):
    if isinstance(primary, str):
        primary = (primary,)

    fields = table[0]
    assert all(
        field in fields for field in primary
    ), f"all primary fields '{primary}' not in '{fields}'"

    order = tuple(
        fields.index(field) for field in sorted(fields) if field in primary
    ) + tuple(fields.index(field) for field in sorted(fields) if field not in primary)
    assert len(fields) == len(order)

    return list(list(row[i] for i in order) for row in table)


def _table_dict(primary: list[str], table: list[list[str]]):
    table = _rotate_fields(primary, table)
    fields = ",".join(table[0])
    rows = table[1:]

    dct = {}
    for row in rows:
        key = ",".join(row[: len(primary)])
        val = ",".join(row[len(primary) :])
        dct[key] = val

    return fields, dct


def _calculate_table_diff(identifier, primary, new, old):
    fields, new = _table_dict(primary, new)
    _, old = _table_dict(primary, old)

    diff = [identifier, fields]
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

    return insertions, deletions, modifications, diff


def _get_head(workdir: str):
    path = os.path.join(workdir, "HEAD")
    if os.path.isfile(path):
        with open(path, "r") as f:
            head = f.read()
        assert re.fullmatch(r"[0-9a-f]{40}", head), f"Bad hash from HEAD: {head}"
        return head
    return None


def _set_head(workdir: str, head: str):
    assert re.fullmatch(r"[0-9a-f]{40}", head), f"Bad hash from HEAD: {head}"
    path = os.path.join(workdir, "HEAD")
    with open(path, "w") as f:
        f.write(head)


def _load_blocks_until(block: Block, hash: str):
    assert re.fullmatch(r"[0-9a-f]{40}", hash), f"Bad hash: {hash}"
    blocks = []
    while block is not None:
        blocks.insert(0, block)
        block = Block.load(block.parent)
    return blocks

def _table_from_diff(current, diffs: str):
    pass


def commit(instance: LCH_Instance):
    # Load new tables
    new = {}
    for table in instance.tables:
        new[table.src] = (table.primary, table.load(table.src))

    # Load old tables
    head = _get_head(instance.work_dir)
    if head is None:
        # Generate fake empty tables
        old = {key: (val[0], val[1][:1]) for key, val in new.items()}
        head = "0" * 40
    else:
        block = Block.load(head)
        blocks = _load_blocks_until(block, "0" * 40)
        old = {}
        for block in blocks:
            pass

        return 0

    diffs = []
    insertions, deletions, modifications = 0, 0, 0
    for source in new.keys():
        primary, new_table = new[source]
        _, old_table = old[source]
        i, d, m, diff = _calculate_table_diff(source, primary, new_table, old_table)
        insertions += i
        deletions += d
        modifications += m
        diffs += diff
        log.info(
            f"Calculated diff for '{source}' containing {i} insertions, {d} deletions, {m} modifications"
        )
    log.info(
        f"Total: {insertions} insertions, {deletions} deletions, {modifications} modifications"
    )

    log.debug("Calculated diff:\n%s" % "\n".join(line for line in diffs))

    data = "\n".join(diffs)
    block = Block(head, str(datetime.datetime.now()), data)
    log.debug("Created block:\n%s" % block)
    block.store()

    _set_head(instance.work_dir, block.id)
