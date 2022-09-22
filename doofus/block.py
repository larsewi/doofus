import hashlib
from functools import cached_property

hasher = hashlib.sha1()


class Block:
    def __init__(self, parent: str, timestamp: str, data: str):
        self._parent = parent
        self._timestamp = timestamp
        self._data = data

    def marshal(self) -> str:
        "\n".join(self._parent, self._timestamp, self._data)

    @staticmethod
    def unmarshal(block: str):
        parent, timestamp, data = block.split("\n", 3)
        return Block(parent, timestamp, data)

    @cached_property
    def id(self) -> str:
        block = self.marshal()
        hasher.update(block)
        hash = hasher.hexdigest()
        return hash

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
        if self._parent == "0":
            raise StopIteration
        return Block.load(self._parent)

    def __str__(self) -> str:
        return "\n".join(
            f"Block id   {str(self.id)}",
            f"Parent id  {str(self.parent)}",
            f"Timestamp  {str(self.timestamp)}",
            f"Data       {len(self.data)} Byte(s)",
        )