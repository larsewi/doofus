import argparse

from doofus.commands import (
    bootstrap_command,
    commit_command,
    fetch_command,
    stop_command,
    track_command,
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

    track = subparsers.add_parser("track", help="track changes in files")
    track.add_argument("file", nargs="+", help="files to track")
    track.set_defaults(func=lambda args: track_command(args.file))

    bootstrap = subparsers.add_parser("bootstrap", help="start serverd deamon and bootstrap to a host")
    bootstrap.add_argument("ip", help="target ip address")
    bootstrap.set_defaults(func=lambda args: bootstrap_command(args.ip))

    commit = subparsers.add_parser("commit", help="commit changes in tracked files")
    commit.set_defaults(func=lambda _: commit_command())

    fetch = subparsers.add_parser("fetch", help="fetch changes from bootstrapped hosts")
    fetch.set_defaults(func=lambda _: fetch_command())

    stop = subparsers.add_parser("stop", help="stop serverd deamon started by bootstrap")
    stop.set_defaults(func=lambda _: stop_command())

    return parser.parse_args()
