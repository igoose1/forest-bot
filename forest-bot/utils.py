import collections
import copy
import dataclasses
import logging
import os
import sys
import time
import typing

__all__ = ("Env",)

logger = logging.getLogger()


async def nop():
    pass


class Fail:
    """Empty class indicates it's necessary to fail."""


class Env:
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
            sys.exit(7)
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


@dataclasses.dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.micro}"


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
