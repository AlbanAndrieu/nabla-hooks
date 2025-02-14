import re

from hooks import __version__


def test_version():
    # assert __version__ == '1.0.2'
    assert re.match(r"^1.0.6.+$", __version__)  # nosec
