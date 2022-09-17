# Copyright 2022 Oskar Sharipov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import logging

from .utils import Env, VersionInfo

__all__ = ("FOREST_CHAT_ID", "bot", "__version__")

__version__ = VersionInfo(2, 2, 1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

env = Env()
API_ID = env.int("API_ID")
API_HASH = env("API_HASH")
BOT_TOKEN = env("BOT_TOKEN")
FOREST_CHAT_ID = env.int("FOREST_CHAT_ID")
IS_DEBUG = env.int("DEBUG", 0)

if IS_DEBUG:
    __version__.set_debug()

HELP_TEXT = f"""Everything will be fine.

[forest-bot](https://github.com/igoose1/forest-bot): {__version__}"""

STICKER_WHITELIST = {
    "AgADJQADaX7FLQ",
    "AgADBBUAAugL-Uo",
    "AgAD-wcAAlwCZQM",
    "AgAD3AsAAt8K6Uo",
    "AgADDAsAAo0jmUs",
    "AgADJgEAAiI3jgQ",
    "AgADBBsAAqbjGEg",
    "AgADMgUAAj-VzAo",
    "AgADHQ0AAkz0uUo",
    "AgAD3wADq1fECw",
}

PUNISHMENT_DURATION = datetime.timedelta(minutes=30)
THROTTLING_RATE = env.int("THROTTLING_RATE", 130)
THROTTLING_PERIOD = env.float("THROTTLING_PERIOD", 55.0)
