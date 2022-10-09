import socket
from doofus.definition import create_leech_instance
from doofus.serverd import serverd
from doofus.hubd import hubd
from doofus.utils import HUBD_PORT, SERVERD_PORT, recv, send
from doofus.leech import _load_tables, _store_tables


def start_command(name) -> int:
    if isinstance(name, list):
        ret = 0
        for n in name:
            ret |= start_command(n)
        return ret

    if name == "serverd":
        ret = serverd.start(SERVERD_PORT)
    else:
        assert name == "hubd", f"Expected 'serverd' or 'hubd' not '{name}'"
        ret = hubd.start(HUBD_PORT)

    return ret

def bootstrap_command(host) -> int:
    with socket.socket() as s:
        s.connect(("localhost", SERVERD_PORT))
        send(s, f"bootstrap {host} {HUBD_PORT}")
        ret = recv(s)

    return ret


def commit_command() -> int:
    instance = create_leech_instance()
    _load_tables(instance.tables)
    _store_tables(instance.tables)
    return 0


def fetch_command() -> int:
    with socket.socket() as s:
        s.connect(("localhost", HUBD_PORT))
        send(s, "fetch")
        ret = recv(s)

    return ret


def stop_command(name):
    if isinstance(name, list):
        ret = 0
        for n in name:
            ret |= stop_command(n)
        return ret

    if name == "serverd":
        port = SERVERD_PORT
    else:
        assert name == "hubd", f"Expected 'serverd' or 'hubd' not '{name}'"
        port = HUBD_PORT

    with socket.socket() as sock:
        sock.connect(("localhost", port))
        send(sock, "exit")
        ret = recv(sock) 

    return ret
