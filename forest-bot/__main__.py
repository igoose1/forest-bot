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
