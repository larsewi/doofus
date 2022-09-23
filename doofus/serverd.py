import os
import signal
import logging as log
from socket import socket
from daemons import daemonizer

from doofus.utils import port, work_dir

SHOULD_RUN = True


def _stop_serverd():
    global SHOULD_RUN
    SHOULD_RUN = False


@daemonizer.run(
    "/tmp/doofus.pid", signals={signal.SIGTERM: [_stop_serverd]}
)
def serverd():
    sock = socket()
    sock.bind(("", port()))
    sock.listen(10)

    while SHOULD_RUN:
        conn, addr = sock.accept()
        log.debug(f"Got a connection from {addr}")
        msg = conn.read()
        log.debug(f"Received message: {msg}")
        conn.close()
