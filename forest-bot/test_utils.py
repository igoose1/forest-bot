import pytest

from .utils import Env, VersionInfo, is_shout


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("AAaaA", True),
        ("not shout", False),
        ("αααααααα AA Аа", True),  # last "Аа" is cyrillic
        (" A A ", False),
    ],
)
def test_is_shout(text, expected):
    assert is_shout(text) is expected


@pytest.mark.parametrize(
    ("version", "result"),
    [
        (VersionInfo(1, 2, 3), "v1.2.3"),
        (VersionInfo(10, 0, 10), "v10.0.10"),
    ],
)
def test_version_info_str(version, result):
    assert str(version) == result


@pytest.fixture()
def patched_env(monkeypatch):
    monkeypatch.setenv("ADDED", "TEST")
    monkeypatch.setenv("ADDED_INT", "123")
    monkeypatch.delenv("REMOVED", raising=False)
    return Env()


def test_env_with_fail(patched_env):
    assert patched_env("ADDED")
    with pytest.raises(SystemExit) as e:
        patched_env("REMOVED")
    assert e.type == SystemExit
    assert e.value.code == 7


def test_env_with_default(patched_env):
    assert patched_env("REMOVED", "DEFAULT") == "DEFAULT"


def test_env_with_int_casting(patched_env):
    assert isinstance(patched_env.int("ADDED_INT"), int)
    with pytest.raises(SystemExit) as e:
        patched_env.int("ADDED")
    assert e.type == SystemExit
    assert e.value.code == 7
