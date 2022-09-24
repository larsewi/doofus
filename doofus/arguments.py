import argparse

from doofus.commands import (
    bootstrap_command,
    track_command,
    commit_command,
    rebase_command,
    kill_command,
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

    track = subparsers.add_parser("track", help="add files to track")
    track.add_argument("file", nargs="+", help="files to track")
    track.set_defaults(func=lambda args: track_command(args.file))

    commit = subparsers.add_parser("commit", help="commit changes")
    commit.set_defaults(func=lambda _: commit_command())

    rebase = subparsers.add_parser("rebase", help="incorporate changes")
    rebase.set_defaults(func=lambda _: rebase_command())

    kill = subparsers.add_parser("kill", help="kill daemons")
    kill.set_defaults(func=lambda _: kill_command())

    return parser.parse_args()
