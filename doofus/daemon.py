import os
import sys
import signal
import socket
import argparse
import logging as log
from abc import ABC, abstractmethod
from argparse import ArgumentParser

from doofus.utils import recv, send


class daemon(ABC):
    class error(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    def __init__(self, pidfile, port):
        self.pidfile = pidfile
        self.port = port
        self.should_run = True

    @property
    def name(self):
        return type(self).__name__

    def daemonize(self):
        if os.path.isfile(self.pidfile):
            raise daemon.error(f"Daemon {self.name} is already running")

        pid = os.fork()
        if pid > 0:
            return

        os.setsid()

        pid = os.fork()
        if pid > 0:
            sys.exit(0)

        pid = os.getpid()
        with open(self.pidfile, "w") as f:
            f.write(str(pid))

        class Killed(Exception):
            def __init__(self, signum) -> None:
                super().__init__(f"Killed with signal {signum}")

        def signal_handler(signum, _):
            raise Killed(signum)

        signal.signal(signal.SIGTERM, signal_handler)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", self.port))
        sock.listen(8)
        log.debug(f"{self.name}: Listening on port {self.port}")

        parser = self.get_parser()
        try:
            while self.should_run:
                conn, addr = sock.accept()
                log.debug(f"{self.name}: Connection from '{addr[0]}:{addr[1]}'")
                req = recv(conn).strip().split()
                try:
                    args = parser.parse_args(req)
                    args.addr = addr
                except argparse.ArgumentError:
                    send(conn, 1)
                else:
                    res = args.action(args)
                    send(conn, res)
                conn.close()
        except:
            ret = 1
        else:
            ret = 0
        finally:
            sock.close()
            os.remove(self.pidfile)
            log.debug(f"{self.name}: daemon stopped")
            sys.exit(ret)

    @abstractmethod
    def get_parser(self) -> ArgumentParser:
        pass

    def exit(self):
        self.should_run = False
        return 0
