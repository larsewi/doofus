import os

from doofus.utils import work_dir


class Head:
    @classmethod
    def get() -> str:
        path = Head._path()
        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read()
        return "0"

    @classmethod
    def set(id: str):
        path = Head._path()
        with open(path, "w") as f:
            f.write(id)

    @classmethod
    def _path():
        return os.path.join(work_dir(), "HEAD")
