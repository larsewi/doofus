import argparse

from doofus.commands import (
    start_command,
    bootstrap_command,
    commit_command,
    fetch_command,
    stop_command,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Doofus leech experiment")
    parser.add_argument(
        "-d",
        "--log-debug",
        action="store_true",
        help="enable debug log messages",
    )

    subparsers = parser.add_subparsers(title="commands")

    start = subparsers.add_parser("start", help="start deamons")
    start.set_defaults(action=lambda _: start_command())

    bootstrap = subparsers.add_parser("bootstrap", help="bootstrap to host")
    bootstrap.add_argument("host", nargs="+", help="ip address or hostname")
    bootstrap.set_defaults(action=lambda args: bootstrap_command(args.host))

    commit = subparsers.add_parser("commit", help="commit changes")
    commit.set_defaults(action=lambda _: commit_command())

    fetch = subparsers.add_parser("fetch", help="fetch changes")
    fetch.set_defaults(action=lambda _: fetch_command())

    stop = subparsers.add_parser("stop", help="stop daemons")
    stop.set_defaults(action=lambda _: stop_command())

    return parser.parse_args()
