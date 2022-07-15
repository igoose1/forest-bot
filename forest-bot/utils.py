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

import collections
import copy
import dataclasses
import logging
import os
import sys
import time
import typing

from unidecode import unidecode

__all__ = ("Env", "Throttle", "VersionInfo", "is_shout")

logger = logging.getLogger("utils")


def is_shout(text: str) -> bool:
    """Returns whether text looks like a shout.

    It is if the following is true:

        * text only consists of "A", "a" or whitespaces and new lines after
        unicode decoding;
        * whitespaces and new lines take less or equal than a half space."""

    decoded_text = unidecode(text).lower()
    return (
        bool(decoded_text)
        and all(map(lambda symbol: symbol in "a \n", decoded_text))
        and len(decoded_text) == len(text)
        and decoded_text.count("a") / len(decoded_text) >= 0.5
    )


async def nop():
    pass


class Fail:
    """Empty class indicates it's necessary to fail."""


class Env:
    fail_status_code = 7

    def __init__(self):
        self.envs = copy.copy(os.environ)

    def __call__(
        self,
        variable_name: str,
        default: str | Fail = Fail,
    ) -> str | typing.NoReturn:
        """Returns environment variable, default or exits with status code 7 if
        default is Fail."""

        if (value := self.envs.get(variable_name, default)) is Fail:
            logger.error("variable %s wasn't set.", variable_name)
            sys.exit(self.fail_status_code)
        return value

    def int(
        self,
        variable_name: str,
        default: int | Fail = Fail,
    ) -> int | typing.NoReturn:
        value = self(variable_name, default)
        try:
            return int(value)
        except ValueError:
            logger.error(
                "variable %s(=%s) can't be casted to int.",
                variable_name,
                value,
            )
            sys.exit(self.fail_status_code)

    def float(
        self,
        variable_name: str,
        default: float | Fail = Fail,
    ) -> int | typing.NoReturn:
        value = self(variable_name, default)
        try:
            return float(value)
        except ValueError:
            logger.error(
                "variable %s(=%s) can't be casted to float.",
                variable_name,
                value,
            )
            sys.exit(self.fail_status_code)


@dataclasses.dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.micro}"


class Throttle:
    """Simple throttling."""

    cache_limit = 10_000

    def __init__(self, rate: int, period: int):
        self._rate = rate
        self._period = period
        self._cache = collections.defaultdict(collections.deque)

    @property
    def rate(self):
        return self._rate

    @property
    def period(self):
        return self._period

    def __call__(self, key: typing.Hashable) -> bool:
        """Returns whether new request must be processed."""
        self.ensure_cache_limit()
        now = time.time()
        self._cache[key].append(now)
        while self._cache[key]:
            if now - self._cache[key][0] < self.period:
                break
            self._cache[key].popleft()
        return len(self._cache[key]) <= self.rate

    def ensure_cache_limit(self) -> None:
        if len(self._cache) <= self.cache_limit:
            return
        now = time.time()
        for key in self._cache:
            if now - self._cache[key][-1] > self.period:
                del self._cache[key]
