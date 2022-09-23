import os
import signal
import logging as log
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
from daemons import daemonizer
from doofus.utils import work_dir

SHOULD_RUN = True
PIDFILE = "/tmp/doofus.pid"
PORT = 39211

def _run_loop():
    global SHOULD_RUN
    SHOULD_RUN = True

    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("", PORT))
    sock.listen(10)
    log.info(f"Listening on port {PORT}.")

    while SHOULD_RUN:
        conn, addr = sock.accept()
        log.debug(f"Got a connection from {addr}.")
        msg = conn.recv(4096).decode()
        header = msg.strip().split("\n", 2)
        if header.strip() == "bootstrap request":
            pass
        conn.close()

def _stop_loop(signum, frame):
    global SHOULD_RUN
    SHOULD_RUN = False
    os.remove(serverd_pidfile())

def serverd_pidfile():
    return os.path.join(work_dir(), "doofus.pid")

def serverd_pid():
    if not os.path.isfile(serverd_pidfile()):
        return None

    with open(serverd_pidfile(), "r") as f:
        pid = int(f.read().strip())

    return pid

def serverd_start():
    if serverd_pid() is not None:
        log.debug(f"Serverd is already running with pid {serverd_pid()}.")       

    pid = os.fork()
    if pid > 0:
        return

    os.setsid()

    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    pid = os.getpid()
    with open(serverd_pidfile(), "w") as f:
        f.write(f"{pid}")
    log.debug(f"Succesfully started serverd {pid}.")

    signal.signal(signal.SIGTERM, _stop_loop)
    _run_loop()

def serverd_stop():
    pid = serverd_pid()
    if pid is None:
        log.debug("Serverd is not running.")
        return

    os.kill(pid, signal.SIGTERM)
    log.info(f"Succesfully stopped serverd {pid}")
