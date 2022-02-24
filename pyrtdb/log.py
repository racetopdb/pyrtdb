import logging
import threading

RTDB_LOGGER: logging.Logger = None
RTDB_LOGGER_NAME = "Rtdb"
RTDB_LOGGER_LEVEL = logging.DEBUG
RTDB_LOGGER_FMT = '[%(levelname)s] %(asctime)s %(name)s <%(processName)s,%(threadName)s> %(module)s@%(lineno)d: %(message)s'
LOGGER_singleton_LOCK = threading.Lock()


def rtdb_logger_singleton(name=RTDB_LOGGER_NAME, level=RTDB_LOGGER_LEVEL) -> logging.Logger:
    global RTDB_LOGGER
    if not RTDB_LOGGER:
        with LOGGER_singleton_LOCK:
            if not RTDB_LOGGER:
                    RTDB_LOGGER = logging.getLogger(name)
                    RTDB_LOGGER.setLevel(level)
                    sh = logging.StreamHandler()
                    sh.setLevel(level)
                    ft = logging.Formatter(fmt=RTDB_LOGGER_FMT)
                    sh.setFormatter(ft)
                    RTDB_LOGGER.addHandler(sh)

    return RTDB_LOGGER


if __name__ == "__main__":
    rtdb_logger_singleton().info("hello world")

