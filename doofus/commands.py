from doofus.serverd import serverd
from doofus.hubd import hubd


def start_command() -> int:
    ret = serverd.start()
    ret |= hubd.start()
    return ret


def bootstrap_command(host: list) -> int:
    return 0 if all(serverd.bootstrap(h) for h in host) else 1


def commit_command() -> int:
    return 1


def fetch_command() -> int:
    return hubd.fetch()


def stop_command():
    hubd.stop()
    serverd.stop()
    return 0
