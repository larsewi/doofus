import logging as log


def bootstrap_command(ip):
    log.debug("command: bootstrap %s" % ip)


def commit_command():
    log.debug("command: commit")


def fetch_command():
    log.debug("command: fetch")


def track_command(file):
    log.debug("command: track")
