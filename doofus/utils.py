import os

SERVERD_PORT = 42101
HUBD_PORT = 42102

def work_dir():
    path = ".leech"
    os.makedirs(path, exist_ok=True)
    return path


def object_dir():
    path = os.path.join(work_dir(), "object")
    os.makedirs(path, exist_ok=True)
    return path
