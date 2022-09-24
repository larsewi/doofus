import os
import logging as log
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from doofus.daemon import Daemon
from doofus.utils import work_dir

class Hubd(Daemon):
    def __init__(self, port):
        self.port = port
        pidfile = os.path.join(work_dir(), "hubd.pid")
        super().__init__(pidfile)

    def _init(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(("", self.port))
        self.sock.listen(10)
        log.debug(f"Listening on port {self.port}.")

    def _loop(self):
        conn, addr = self.sock.accept()
        log.debug("Got a connection from %s:%s." % addr)
        msg = conn.recv(4096).decode()

        try:
            header, payload = msg.split("\n", 2)
        except:
            header, payload = (msg, None)

        if header == "bootstrap request":
            path = os.path.join(work_dir(), "known_hosts")
            if os.path.isfile(path):
                with open(path, "r") as f:
                    hosts = f.readlines()
                if any(host.strip() == str(addr) for host in hosts):
                    conn.send("bootstrap rejected".encode())
                    conn.close()
                    return

            ip, _ = addr
            with open(path, "w") as f:
                f.write(f"{ip}")
            conn.send("bootstrap accepted".encode())
        else:
            conn.send("bad request".encode())

        conn.close()

    def _exit(self):
        pass
