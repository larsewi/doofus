import os
import socket
import logging as log
from doofus.daemon import Daemon
from doofus.utils import HUBD_PORT, work_dir

class Serverd(Daemon):
    def __init__(self, port):
        self.port = port
        pidfile = os.path.join(work_dir(), "serverd.pid")
        super().__init__(pidfile)

    def _init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", self.port))
        self.sock.listen(10)
        log.debug(f"Listening on port {self.port}.")

    def _loop(self):
        conn, addr = self.sock.accept()
        log.debug("Got a connection from %s:%s." % addr)
        msg = conn.recv(4096).decode()

        if msg.startswith("bootstrap "):
            sock = socket.socket()
            sock.connect((msg[len("bootstrap "):], HUBD_PORT))
            sock.send("bootstrap request".encode())
            msg = sock.recv(4096)
            sock.close()
            conn.send(msg)
        else:
            conn.send("bad request".encode())

        conn.close()

    def _exit(self):
        pass
