import argparse
import os
import logging as log
from doofus.daemon import daemon
from doofus.utils import work_dir

class hubd(daemon):
    def __init__(self, port):
        pidfile = os.path.join(work_dir(), "hubd.pid")
        super().__init__(pidfile, port)
        self.hosts = []

    def get_parser(self):
        parser = argparse.ArgumentParser(prog="hubd", exit_on_error=False)
        subparsers = parser.add_subparsers()

        bootstrap = subparsers.add_parser("bootstrap")
        bootstrap.add_argument("port", type=int)
        bootstrap.set_defaults(action=lambda args: self.bootstrap(args.addr[0], args.port))

        fetch = subparsers.add_parser("fetch")
        fetch.add_argument("port", type=int)
        fetch.set_defaults(action=lambda args: self.fetch(args.conn, args.port))

        exit = subparsers.add_parser("exit")
        exit.set_defaults(action=lambda _: self.exit())

        return parser

    @staticmethod
    def start(port):
        hubd(port).daemonize()
        return 0

    def bootstrap(self, host, port):
        self.hosts.append((host, port))
        log.debug(f"hubd: Added '{host}:{port}' to bootstrapped hosts.")
        return 0

    def fetch(self, port):
        return 0
