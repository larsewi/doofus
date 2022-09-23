import logging as log
import os

from doofus.serverd import serverd
from doofus.utils import work_dir


def bootstrap_command(ip):
    os.makedirs(work_dir(), exist_ok=True)
    serverd()


def commit_command():
    pass


def fetch_command():
    pass


def stop_command():
    serverd.stop()


def track_command(file):
    pass
