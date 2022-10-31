import os
import hashlib
from functools import cached_property
from doofus.utils import object_dir


class Block:
    def __init__(self, parent: str, timestamp: str, data: str):
        self._parent = parent
        self._timestamp = timestamp
        self._data = data

        block = self.marshal()
        block = block.encode("utf-8")
        hasher = hashlib.sha1()
        hasher.update(block)
        hash = hasher.hexdigest()
        self._id = hash

    @staticmethod
    def load(id):
        path = os.path.join(object_dir(), id[:2], id[2:])
        if os.path.isfile(path):
            with open(path, "r") as f:
                block = f.read()
            return Block.unmarshal(block)
        return None

    def store(self):
        id = self.id
        path = os.path.join(object_dir(), id[:2])
        os.makedirs(path, exist_ok=True)
        path = os.path.join(path, id[2:])
        block = self.marshal()
        with open(path, "w") as f:
            f.write(block)
        return id

    def marshal(self) -> str:
        return "\n".join((self._parent, self._timestamp, self._data))

    @staticmethod
    def unmarshal(block: str):
        parent, timestamp, data = block.split("\n", 3)
        return Block(parent, timestamp, data)

    @cached_property
    def id(self) -> str:
        return self._id

    @property
    def parent(self) -> str:
        return self._parent

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @property
    def data(self) -> str:
        return self._data

    def __iter__(self):
        return self

    def __next__(self):
        if self._parent == "0" * 40:
            raise StopIteration
        return Block.load(self._parent)

    def __str__(self) -> str:
        return "\n".join(
            (
                f"Block id   {str(self.id)}",
                f"Parent id  {str(self.parent)}",
                f"Timestamp  {str(self.timestamp)}",
                f"Data       {len(self.data)} Byte(s)",
            )
        )
