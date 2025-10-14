import re

from hooks import __version__


def test_version():
    # assert __version__ == 'v1.0.6-65-g82cbbe7'

    # assert re.match(r"^0\+(untagged|unknown).*.+$", "v1.0.6-65-g82cbbe7")  # nosec
    assert re.match(r"^0\+(untagged|unknown)(.+)?$", "0+unknown")  # nosec
    assert re.match(r"^0\+(untagged|unknown)(.+)?$", __version__)  # nosec

    __version_test__ = "v1.0.6"
    assert __version_test__ == "v1.0.6"

    assert re.match(r"^v1.0.6?.+$", __version_test__)  # nosec
    assert re.match(r"^v\d{1,5}\.\d{1,5}\.\d{1,5}$", __version_test__)  # nosec
