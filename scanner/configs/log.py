from loguru import logger
import sys

logger.remove(0)

logger.add(
    sys.stderr,
    colorize=True,
    format=
    "<blue>{time:HH:mm:ss}</blue> | <level>{level: <8}</level> | <level>{message}</level>", enqueue=True
    )
