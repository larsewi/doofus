import os
import json
import re

def LCH_LoadCSV():
    pass

def LCH_StoreCSV():
    pass

class LCH_Table:
    def __init__(self, locator, *, load_fn=LCH_LoadCSV, store_fn=LCH_StoreCSV):
        pass

class LCH_Instance:
    def __init__(self):
        pass

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
