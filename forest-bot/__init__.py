import datetime
import logging

from .utils import Env, VersionInfo

__all__ = ("FOREST_CHAT_ID", "bot", "__version__")

__version__ = VersionInfo(2, 0, 0)

logging.basicConfig(level=logging.INFO)

env = Env()
API_ID = env.int("API_ID")
API_HASH = env("API_HASH")
BOT_TOKEN = env("BOT_TOKEN")
FOREST_CHAT_ID = env.int("FOREST_CHAT_ID")

HELP_TEXT = f"""Everything will be fine.

[forest-bot](https://github.com/igoose1/forest-bot): {__version__}"""

PUNISHMENT_DURATION = datetime.timedelta(minutes=30)
THROTTLING_RATE = env.int("THROTTLING_RATE", 130)
THROTTLING_PERIOD = env.float("THROTTLING_PERIOD", 55.0)
