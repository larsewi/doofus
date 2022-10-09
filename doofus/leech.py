from asyncore import read
import os
import re
import csv
import json
from doofus.block import Block

from doofus.utils import work_dir

def LCH_LoadTableCSV(path):
    """
    Load a csv table as a two dimentional list where the first row contains
    the field names and the remaining rows contain the data. E.g.
    [
        [id, lastname, firstname, born],
        [ 1,     Bond,     James, 1953],
        [ 2,    Wayne,     Bruce, 1939]
    ]
    """
    if not os.path.isfile(path):
        return None
    with open(path, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    return rows

def LCH_StoreTableCSV(path, rows):
    """
    Store a two dimentional list as csv where the first row contains the field
    names and the remaining rows contain the data. E.g.
    [
        [id, lastname, firstname, born],
        [ 1,     Bond,     James, 1953],
        [ 2,    Wayne,     Bruce, 1939]
    ]
    """
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
            print(key)
            print(val)
            table.data[key] = val

def _store_tables(tables: list[LCH_Table]):
    for table in tables:
        rows = [table.fields]
        for key, val in table.data.items():
            rows.append(key.split(",") + val.split(","))
        table.store(table.dest, rows)

def _get_head(workdir):
    path = os.path.join(work_dir, "HEAD")
    if not os.path.isfile(path):
        return None

def commit(instance: LCH_Instance):
    old = _load_tables(instance.tables)

    head = _get_head(instance.work_dir)
    if head is None:
        new = old
    else:
        chain = [block for block in Block.load(head)]
