import os
import logging as log
from datetime import datetime

from doofus.block import Block
from doofus.head import Head
from doofus.serverd import serverd
from doofus.utils import object_dir


def bootstrap(ip):
    pass


def commit(data):
    parent_id = Head.get()
    timestamp = datetime.now()
    child = Block(parent_id, timestamp, data)
    log.debug(f"Created block:\n{child}")

    path = os.path.join(object_dir(), child.id[:2], child.id[2:])
    block = child.marshal()
    with open(path, "w") as f:
        log.debug(f"Writing block to {path}:")
        f.write(block)

    log.debug(f"Moving head from {parent_id} to {child.id}")
    Head.set(child.id)
