import os
import sys
import signal
import logging as log
from abc import ABC, abstractmethod


class Daemon(ABC):
    def __init__(self, pidfile):
        self._pidfile = pidfile

    @property
    def pid(self):
        try:
            with open(self._pidfile, "r") as f:
                pid = int(f.read().strip())
        except:
            return None
        return pid

    @pid.setter
    def pid(self, val):
        with open(self._pidfile, "w") as f:
            f.write(str(val))

    def start(self):
        if self.pid is not None:
            log.debug(f"Deamon {self._pidfile} is already running.")
            return

        pid = os.fork()
        if pid > 0:
            return

        os.setsid()

        pid = os.fork()
        if pid > 0:
            sys.exit(0)

        with open(self._pidfile, "w") as f:
            f.write(str(os.getpid()))

        should_run = True
        def sigterm_handler(signum, frame):
            nonlocal should_run
            should_run = False
        signal.signal(signal.SIGTERM, sigterm_handler)

        self._init()
        while should_run:
            self._loop()
        self._exit()

    def stop(self):
        os.kill(self.pid, signal.SIGTERM)

    @abstractmethod
    def _init():
        pass

    @abstractmethod
    def _loop(msg):
        pass

    @abstractmethod
    def _exit():
        pass
