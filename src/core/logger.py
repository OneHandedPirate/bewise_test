import logging
from logging.handlers import RotatingFileHandler

from src.core.config import BASE_DIR


logger: logging.Logger = logging.Logger("custom", level=logging.INFO)
formatter: logging.Formatter = logging.Formatter(
    "%(levelname)s [%(asctime)s] %(funcName)s | %(lineno)d | %(message)s"
)
handler: RotatingFileHandler = RotatingFileHandler(
    f"{BASE_DIR}/logs/logs.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False