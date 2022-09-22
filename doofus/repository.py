import os
import hashlib
import logging as log

def work_dir():
    return ".leech"

def object_dir():
    return os.path.join(work_dir(), "object")

def init_repository():
    os.makedirs(work_dir(), exist_ok=True)

def commit(timestamp, parent, data):
    block = f"{timestamp}\n{parent}\n{data}\n".encode("utf-8")
    hasher = hashlib.sha1()
    hasher.update(block)
    id = hasher.hexdigest()
    log.debug(f"Generated block with id '{id}'")

    path = os.path.join(object_dir(), id[:2], id[2:])
    with open(path, "w") as f:
        log.debug(f"Writing block to file '{path}'")
        f.write(block)

    head = os.path.join(work_dir(), "HEAD")
    with open(head, "w") as f:
        log.debug(f"Updating '{head}' to '{id}'")
        f.write(id)
