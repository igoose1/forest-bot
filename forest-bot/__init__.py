import datetime
import logging

from telethon import TelegramClient

from .utils import Env, VersionInfo

__all__ = ("FOREST_CHAT_ID", "bot", "__version__")

__version__ = VersionInfo(0, 0, 4)

logging.basicConfig(level=logging.INFO)

env = Env()
API_ID = env.int("API_ID")
API_HASH = env("API_HASH")
BOT_TOKEN = env("BOT_TOKEN")
FOREST_CHAT_ID = env.int("FOREST_CHAT_ID")
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

HELP_TEXT = f"""Everything will be fine.

forest-bot: {__version__}"""

PUNISHMENT_DURATION = datetime.timedelta(hours=1)
THROTTLING_RATE = 100
THROTTLING_PERIOD = 120.0
