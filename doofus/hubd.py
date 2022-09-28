import os
import logging as log
from doofus.daemon import daemon
from doofus.utils import work_dir

class hubd:
    @staticmethod
    def pidfile():
        return os.path.join(work_dir(), "serverd.pid")

    @staticmethod
    def port():
        return 2021

    @staticmethod
    def start():
        try:
            daemon.start(hubd.pidfile(), hubd.port(), hubd._event)
        except Exception as e:
            log.error(f"Failed to start hubd: {e}.")
            return 1
        log.info("Successfully started hubd.")
        return 0

    @staticmethod
    def stop():
        try:
            daemon.stop(hubd.pidfile())
        except Exception as e:
            log.error(f"Failed to stop hubd: {e}")
            return 1
        log.info("Successfully stopped hubd.")
        return 0

    @staticmethod
    def fetch():
        pass

    @staticmethod
    def _event(conn, addr):
        pass
