import os
import csv
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
    def __init__(self, unique_id: str|list, src: str, dest: str, load=LCH_LoadTableCSV, store=LCH_StoreTableCSV):
        if isinstance(unique_id, str):
            self.unique_id = unique_id.split(",")
        else:
            self.unique_id = unique_id
        self.src = src
        self.dest = dest
        self.load = load
        self.store = store
        self.fields = []
        self.data = {}

class LCH_Instance:
    def __init__(self, work_dir: str, tables: LCH_Table):
        if not os.path.isdir(work_dir):
            os.mkdir(work_dir)
        self.work_dir = work_dir
        self.tables = tables


def _load_tables(tables: list[LCH_Table]):
    for table in tables:
        rows = table.load(table.src)
        table.fields = rows[0]
        unique = [table.fields.index(f) for f in table.fields if f in table.unique_id]
        non_unique = [table.fields.index(field) for field in table.fields if field not in table.unique_id]

        for row in rows[1:]:
            key = ",".join([row[i] for i in unique])
            val = ",".join([row[i] for i in non_unique])
            table.data[key] = val

def _store_tables(tables: list[LCH_Table]):
    for table in tables:
        rows = [table.fields]
        for key, val in table.data.items():
            rows.append(key.split(",") + val.split(","))
        table.store(table.dest, rows)

def _diff_dict(primary, table):
    fields = table[:1]
    key_index = (fields.index(f) for f in fields if f in primary)
    val_index = (fields.index(f) for f in fields if f not in primary)
    key_val_pairs = (((row[i] for i in key_index), (row[i] for i in val_index)) for row in table)
    dct = {key: val for key, val in key_val_pairs}
    return dct

def _calculate_diff(primary, new, old):
    new = _diff_dict(primary, new)
    old = _diff_dict(primary, old)
    diff = []

    # Rows added from new
    for key in new.keys() - old.keys():
        diff.append(f"+{','.join(key)}:{','.join(new[key])}")

    # Rows removed from new
    for key in new.keys() - old.keys():
        diff.append(f"-{','.join(key)}")

    # Rows changed in new
    for key in new.keys() & old.keys():
        if new[key] != old[key]:
            diff.append(f"%{','.join(key)}:{','.join(new[key])}")

    return diff

def _get_head(workdir):
    path = os.path.join(work_dir, "HEAD")
    if not os.path.isfile(path):
        return None

def commit(instance: LCH_Instance):
    _load_tables(instance.tables)
    new = instance.tables

    head = _get_head(instance.work_dir)