import os
import logging as log
from datetime import datetime

from doofus.block import Block
from doofus.head import Head
from doofus.utils import object_dir, work_dir


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

def track(file, identifier):
    path = os.path.join(work_dir(), "tracking")
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
        tracking = {f: i for f, i in (l.split(":") for l in lines)}
    else:
        tracking = {}

    tracking[file] = identifier

    lines = [f"{f}:{i}" for f, i, in tracking.items()]
    with open(path, "w") as f:
        f.writelines(lines)



def file_diff(path):
    pass
