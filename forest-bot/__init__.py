import logging

from telethon import TelegramClient

from .utils import Env

__all__ = ("FOREST_CHAT_ID", "bot", "version")

logging.basicConfig(level=logging.INFO)

__version__ = (0, 0, 1)

env = Env()
API_ID = env.int("API_ID")
API_HASH = env("API_HASH")
BOT_TOKEN = env("BOT_TOKEN")
FOREST_CHAT_ID = env.int("FOREST_CHAT_ID")
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

HELP_TEXT = """Uncommon beauty is commonly overlooked."""
