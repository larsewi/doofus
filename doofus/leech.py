import os
import csv
from re import A
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
    def __init__(self, primary: str|list, src: str, dest: str, load=LCH_LoadTableCSV, store=LCH_StoreTableCSV):
        if isinstance(primary, str):
            self.primary = primary.split(",")
        else:
            self.primary = primary
        self.src = src
        self.dest = dest
        self.load = load
        self.store = store

class LCH_Instance:
    def __init__(self, work_dir: str, tables: LCH_Table):
        if not os.path.isdir(work_dir):
            os.mkdir(work_dir)
        self.work_dir = work_dir
        self.tables = tables

def _get_indicies(primary, fields):
    keys = [fields.index(f) for f in fields if f in primary]
    vals = [fields.index(f) for f in fields if f not in primary]
    return (keys, vals)

def _diff_dict(primary, table):
    fields = table[0]
    rows = table[1:]
    
    # Sort fields to have primary key first
    key_idx, val_idx = _get_indicies(primary, fields)
    fields = ",".join(fields[i] for i in key_idx + val_idx)

    dct = {}
    for row in rows:
        key = ",".join(row[i] for i in key_idx)
        val = ",".join(row[i] for i in val_idx)
        dct[key] = val

    return fields, dct

def _calculate_diff(primary, new, old):
    fields, new = _diff_dict(primary, new)
    _, old = _diff_dict(primary, old)

    diff = [fields]

    # Rows added from new
    for key in new.keys() - old.keys():
        diff.append(f"+{key},{new[key]}")

    # Rows removed from new
    for key in old.keys() - new.keys():
        diff.append(f"-{key}")

    # Rows changed in new
    for key in new.keys() & old.keys():
        if new[key] != old[key]:
            diff.append(f"%{key},{new[key]}")

    return diff

def _get_head(workdir):
    path = os.path.join(work_dir, "HEAD")
    if os.path.isfile(path):
        with open(path, "r") as f:
            head = f.read(path)
        return head
    return None



def commit(instance: LCH_Instance):
    pass