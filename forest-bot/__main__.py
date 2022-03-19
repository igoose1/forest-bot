import logging

from . import __version__
from .bot import bot

__all__ = ("run",)

logger = logging.getLogger("forest-bot")


def run() -> None:
    logger.info("version: %s", __version__)
    bot.run_until_disconnected()


if __name__ == "__main__":
    run()
