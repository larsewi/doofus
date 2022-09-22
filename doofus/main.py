import argparse
import logging as log


def parse_args():
    parser = argparse.ArgumentParser(description="Doofus leech experiment")
    parser.add_argument(
        "--log-debug",
        help="enable debug logging",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    log.basicConfig(
        format="%(levelname)8s: %(message)s",
        level=log.DEBUG if args.debug else log.INFO,
    )
