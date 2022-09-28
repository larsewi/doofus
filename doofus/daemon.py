from genericpath import isfile
import os
import sys
import socket
import signal


class daemon:
    class error(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    def __init__(self, pidfile, port):
        self._pidfile = pidfile
        self._port = port

    @staticmethod
    def start(pidfile: str, port: int, event_handler):
        if os.path.isfile(pidfile):
            raise daemon.error("Daemon is already running")

        pid = os.fork()
        if pid > 0:
            return

        os.setsid()

        pid = os.fork()
        if pid > 0:
            sys.exit(0)

        pid = os.getpid()
        with open(pidfile, "w") as f:
            f.write(str(pid))

        should_run = True
    
        def signal_handler(signum, frame):
            nonlocal should_run
            should_run = False

        signal.signal(signal.SIGTERM, signal_handler)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", port))
        sock.listen(8)

        try:
            while should_run:
                conn, addr = sock.accept()
                event_handler(conn, addr)
                conn.close()
        finally:
            sock.close()
            os.remove(pidfile)

    @staticmethod
    def stop(pidfile):
        if not os.path.isfile(pidfile):
            raise daemon.error("Daemon is not running")

        with open(pidfile, "r") as f:
            pid = int(f.read())

        os.kill(pid, signal.SIGTERM)
