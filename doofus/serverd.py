import os
import logging as log
from doofus.daemon import daemon
from doofus.utils import work_dir

class serverd:
    @staticmethod
    def pidfile():
        return os.path.join(work_dir(), "serverd.pid")

    @staticmethod
    def port():
        return 2021

    @staticmethod
    def start():
        try:
            daemon.start(serverd.pidfile(), serverd.port(), serverd._event)
        except Exception as e:
            log.error(f"Failed to start serverd: {e}.")
            return 1
        log.info("Successfully started serverd.")
        return 0

    @staticmethod
    def stop():
        try:
            daemon.stop(serverd.pidfile())
        except Exception as e:
            log.error(f"Failed to stop serverd: {e}")
            return 1
        log.info("Successfully stopped serverd.")
        return 0

    def bootstrap(host):
        pass

    @staticmethod
    def _event(conn, addr):
        pass
