import os
import sys
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
