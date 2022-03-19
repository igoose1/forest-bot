import pytest

from .bot import is_shout


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
