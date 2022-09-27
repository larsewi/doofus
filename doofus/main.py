import logging as log

from doofus.arguments import parse_args


def main():
    args = parse_args()
    log.basicConfig(
        format="%(levelname)8s: %(message)s",
        level=log.DEBUG if args.log_debug else log.INFO,
    )
    return args.action(args)
