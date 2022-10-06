import argparse
import os
import logging as log
import socket
from doofus.daemon import daemon
from doofus.utils import recv, send, work_dir

class serverd(daemon):
    def __init__(self, port):
        pidfile = os.path.join(work_dir(), "serverd.pid")
        super().__init__(pidfile, port)

    def get_parser(self):
        parser = argparse.ArgumentParser(prog="serverd", exit_on_error=False)
        subparsers = parser.add_subparsers()

        bootstrap = subparsers.add_parser("bootstrap")
        bootstrap.add_argument("host")
        bootstrap.add_argument("port", type=int)
        bootstrap.set_defaults(action=lambda args: self.bootstrap(args.host, args.port))

        fetch = subparsers.add_parser("fetch")
        fetch.set_defaults(action=lambda args: self.fetch(args.conn))

        exit = subparsers.add_parser("exit")
        exit.set_defaults(action=lambda _: self.exit())

        return parser

    @staticmethod
    def start(port):
        serverd(port).daemonize()
        return 0

    def bootstrap(self, host, port):
        log.debug(f"serverd: Bootstrapping to host '{host}:{port}'")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            send(s, f"bootstrap {self.port}")
            ret = recv(s)
        return ret

    def fetch(self, args):
        return 0
