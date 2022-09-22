import os
import hashlib
import logging as log
from datetime import datetime
from doofus.block import Block
from doofus.head import Head
from doofus.utils import object_dir, work_dir


def init_repository():
    os.makedirs(work_dir(), exist_ok=True)

def commit(data):
    parent = Head.get()
    timestamp = datetime.now()

    child = Block(parent, timestamp, data)
    path = os.path.join(object_dir(), child.id[:2], child.id[2:])
    block = child.marshal()

    with open(path, "w") as f:
        log.debug(f"Writing block to {path}:")
        log.debug(child)
        f.write(block)
