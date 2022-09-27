import os
import sys
import signal
import socket
import logging as log
from abc import ABC, abstractmethod


class Daemon(ABC):
    @property
    def pid(self):
        try:
            with open(self.pidfile, "r") as f:
                pid = int(f.read().strip())
        except:
            return None
        return pid

    @pid.setter
    def pid(self, val):
        with open(self.pidfile, "w") as f:
            f.write(str(val))

    @property
    @abstractmethod
    def port(self):
        pass

    @property
    @abstractmethod
    def pidfile(self):
        pass

    def start(self):
        if self.pid is not None:
            log.debug(f"Deamon {self.pidfile} is already running.")
            return

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

        should_run = True

        def sigterm_handler(signum, frame):
            nonlocal should_run
            should_run = False

        signal.signal(signal.SIGTERM, sigterm_handler)
        log.info(f"Successfully deamonized process {pid}.")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.settimeout(1.5)
                sock.bind(("", self.port))
                sock.listen(8)
                log.debug(f"Listening on port {self.port}.")

                while should_run:
                    try:
                        conn, addr = sock.accept()
                        conn.settimeout(1.5)
                    except socket.timeout:
                        continue
                    log.debug(f"Got a connection from {addr[0]}:{addr[1]}.")
                    self._loop(conn, addr)
                    conn.close()
        finally:
            if os.path.isfile(self.pidfile):
                os.remove(self.pidfile)
            exit(0)

    def stop(self):
        pid = self.pid
        if pid is not None:
            try:
                os.kill(pid, signal.SIGTERM)
                log.info(f"Killed daemon {pid}.")
            except ProcessLookupError as e:
                log.warning(f"Failed to kill process {pid}: {e}")

    @abstractmethod
    def _loop(msg):
        pass
