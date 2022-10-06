import os
import re
import marshal
from socket import socket

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


def get_head():
    path = os.path.join(work_dir(), "HEAD")
    if os.path.isfile(path):
        with open(path, "r") as f:
            head = f.read().strip()
    else:
        head = "0" * 40
    assert re.fullmatch(r"[0-9a-f]{40}", head)
    return head


def set_head(head):
    assert re.fullmatch(r"[0-9a-f]{40}", head)
    path = os.path.join(work_dir(), "HEAD")
    with open(path, "w") as f:
        f.write(head)


def send(sock: socket, data):
    payload = marshal.dumps(data)
    size = len(payload)
    header = size.to_bytes(4, "big")
    sock.send(header + payload)


def recv(sock: socket):
    header = sock.recv(4)
    size = int.from_bytes(header, "big")
    payload = sock.recv(size)
    data = marshal.loads(payload)
    return data
