import copy
import dataclasses
import logging
import os
import sys
import typing

__all__ = ("Env",)

logger = logging.getLogger()


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
