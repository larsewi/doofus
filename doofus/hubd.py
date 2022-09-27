import os
import socket
from doofus.daemon import Daemon
from doofus.utils import recv, send, work_dir


class Hubd(Daemon):
    @property
    def port(self):
        return 2021

    @property
    def pidfile(self):
        return os.path.join(work_dir(), "hubd.pid")

    def _loop(self, conn: socket.socket, addr: tuple):
        req = recv(conn)
        command = req["command"]
        if command == "bootstrap":
            res = self._bootstrap()
        elif command == "fetch":
            res = self._fetch()
        else:
            status = "failure"
            message = f"Bad command '{command}'."
            res = {"status": status, "message": message}
        send(conn, res)

    def _bootstrap(self):
        return {"status": "success", "message": "No operation."}

    def _fetch(self):
        return {"status": "success", "message": "No operation."}
