import os
import signal
from doofus.serverd import PIDFILE, serverd_start, serverd_stop


def bootstrap_command(ip):
    pass


def track_command(file):
    pass


def commit_command():
    pass


def fetch_command():
    with open(PIDFILE, "r") as f:
        pid = int(f.read())
    os.kill(pid, signal.SIGUSR1)


def start_command():
    serverd_start()


def stop_command():
    serverd_stop()
