import logging
import logging.handlers
import os

from rich.logging import RichHandler

RICH_FORMAT = "[%(filename)s:%(lineno)s] >> %(message)s"
FILE_HANDLER_FORMAT = "[%(asctime)s]\t[%(levelname)s] %(message)s\t>>[%(filename)s:%(funcName)s:%(lineno)s]"


def set_logger(log_path: str) -> logging.Logger:
    if not os.path.exists(log_path):
        os.makedirs(os.path.dirname(log_path))

    logging.basicConfig(
        level=logging.INFO,
        format=RICH_FORMAT,
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = logging.getLogger(log_path)

    if len(logger.handlers) > 0:
        return logger

    file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(FILE_HANDLER_FORMAT))
    logger.addHandler(file_handler)

    return logger


def handle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger("rich")

    logger.error("Unexpected exception", exc_info=(exc_type, exc_value, exc_traceback))
