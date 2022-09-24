import socket
import logging as log
from time import sleep
from doofus.serverd import Serverd
from doofus.hubd import Hubd
from doofus.utils import SERVERD_PORT, HUBD_PORT


def bootstrap_command(ip):
    Serverd(SERVERD_PORT).start()
    Hubd(HUBD_PORT).start()

    sleep(1)

    sock = socket.socket()
    sock.connect(("localhost", SERVERD_PORT))
    sock.send(f"bootstrap {ip}".encode())
    msg = sock.recv(4096).decode()
    if msg == "bootstrap accepted":
        log.info(f"Succesfully bootstrapped to {ip}")
    else:
        log.error(f"Failed to bootstrap to {ip}: {msg}")
    sock.close()


def track_command(file):
    pass


def commit_command():
    pass


def rebase_command():
    pass


def kill_command():
    Serverd(SERVERD_PORT).stop()
    Hubd(HUBD_PORT).stop()
