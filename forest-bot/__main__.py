import logging

from . import __version__
from .bot import app

__all__ = ("run",)

logger = logging.getLogger("forest-bot")


def run() -> None:
    logger.info("%s", __version__)
    app.run()


if __name__ == "__main__":
    run()
