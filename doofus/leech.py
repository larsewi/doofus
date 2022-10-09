from asyncore import read
import os
import re
import csv
import json

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
    def __init__(self, tables: LCH_Table):
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


class Leech:
    def __init__(self, data):
        self._data = data

    @property
    @staticmethod
    def work_dir():
        path = ".leech"
        if not os.path.isdir(path):
            os.mkdir(path)
        return path

    @property
    @staticmethod
    def object_dir():
        path = os.path.join(Leech.work_dir, "object")
        if not os.path.isdir(path):
            os.mkdir(path)
        return path

    @staticmethod
    def load():
        path = os.path.join(Leech.work_dir, "leech.json")
        if os.path.isfile(path):
            with open(path, "r") as f:
                data = json.load(f)
        else:
            data = { "head": "0" * 40, "tracked": []}
        return Leech(data)

    def save(self):
        path = os.path.join(Leech.work_dir, "leech.json")
        with open(path, "w") as f:
            json.dump(self._data, f)

    @property
    def head(self) -> str:
        hash = self._data["head"]
        assert re.fullmatch(r"[0-9a-f]{40}", hash)
        return hash

    @head.setter
    def head(self, hash: str):
        assert re.fullmatch(r"[0-9a-f]{40}", hash)
        self._data["head"] = hash

    @property
    def tracked(self) -> list:
        return self._data["tracked"]

    def commit(self):
        pass
