import socket
import logging as log
from doofus.serverd import Serverd
from doofus.hubd import Hubd
from doofus.utils import recv, send


def start_command() -> int:
    Serverd().start()
    Hubd().start()
    return 0


def bootstrap_command(host) -> int:
    if isinstance(host, list):
        return 0 if all(bootstrap_command(h) == 0 for h in host) else 1

    req = {"command": "bootstrap", "host": host}
    try:
        with socket.socket() as sock:
            sock.settimeout(2)
            sock.connect(("localhost", Serverd().port))
            send(sock, req)
            res = recv(sock)
    except socket.error as e:
        log.error(e)
        return 1

    if res["status"] == "success":
        log.info(res["message"])
        return 0
    log.error(res["message"])
    return 1


def commit_command() -> int:
    req = {"command": "commit"}
    try:
        with socket.socket() as sock:
            sock.settimeout(2)
            sock.connect(("localhost", Serverd().port))
            send(sock, req)
            res = recv(sock)
    except socket.error as e:
        log.error(e)
        return 1

    if res["status"] == "success":
        log.info(res["message"])
        return 0
    log.error(res["message"])
    return 1


def fetch_command() -> int:
    req = {"command": "fetch"}
    try:
        with socket.socket() as sock:
            sock.settimeout(2)
            sock.connect(("localhost"), Hubd().port)
            send(sock, req)
            res = recv(sock)
    except socket.error as e:
        log.error(e)
        return 1

    if res["status"] == "success":
        log.info(res["message"])
        return 0
    log.error(res["message"])
    return 1


def stop_command():
    Serverd().stop()
    Hubd().stop()
    return 0
