import logging
import sys
from functools import cache


@cache
def global_logger() -> logging.Logger:
    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)s: %(asctime)s - %(module)s.py (line %(lineno)d) - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger("global")
    logger.setLevel(logging.INFO)
    return logger
