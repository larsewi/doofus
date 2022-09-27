import os
import socket
from doofus.hubd import Hubd
from doofus.daemon import Daemon
from doofus.utils import recv, send, work_dir


class Serverd(Daemon):
    @property
    def port(self):
        return 2022

    @property
    def pidfile(self):
        return os.path.join(work_dir(), "serverd.pid")

    def _loop(self, conn: socket.socket, addr: tuple):
        req = recv(conn)
        command = req["command"]
        if command == "bootstrap":
            res = self._bootstrap(req["host"])
        elif command == "commit":
            res = self._commit()
        else:
            status = "failure"
            message = f"Bad command '{command}'."
            res = {"status": status, "message": message}
        send(conn, res)

    def _bootstrap(self, host):
        status = "failure"
        try:
            with socket.socket() as sock:
                sock.settimeout(1)
                sock.connect((host, Hubd().port))
                req = {"command": "bootstrap"}
                send(sock, req)
                res = recv(sock)
            if res["status"] == "success":
                status = "success"
                message = f"Successfully bootstrapped to '{host}'."
            else:
                message = f"Failed to bootstrap to '{host}': {res['message']}"
        except socket.error as e:
            message = f"Failed to bootstrap to '{host}': {e}"
        return {"status": status, "message": message}

    def _commit(self):
        return {"status": "success", "message": "No operation."}
