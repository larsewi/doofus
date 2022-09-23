import argparse

from doofus.commands import (
    bootstrap_command,
    track_command,
    commit_command,
    fetch_command,
    start_command,
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

    bootstrap = subparsers.add_parser("bootstrap", help="bootstrap to host")
    bootstrap.add_argument("ip", help="target ip address")
    bootstrap.set_defaults(func=lambda args: bootstrap_command(args.ip))

    track = subparsers.add_parser("track", help="track changes in files")
    track.add_argument("file", nargs="+", help="files to track")
    track.set_defaults(func=lambda args: track_command(args.file))

    commit = subparsers.add_parser("commit", help="commit changes in tracked files")
    commit.set_defaults(func=lambda _: commit_command())

    fetch = subparsers.add_parser("fetch", help="fetch changes from known hosts")
    fetch.set_defaults(func=lambda _: fetch_command())

    start = subparsers.add_parser("start", help="start served")
    start.set_defaults(func=lambda _: start_command())

    stop = subparsers.add_parser("stop", help="stop serverd")
    stop.set_defaults(func=lambda _: stop_command())

    return parser.parse_args()
