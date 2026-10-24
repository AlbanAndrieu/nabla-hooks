import re
from importlib.metadata import version

from hooks import __version__


def test_version():
    # Installed (editable) package: version comes from pyproject.toml
    assert __version__ == version("nabla-hooks")
    assert re.match(r"^\d{1,5}\.\d{1,5}\.\d{1,5}", __version__)  # nosec

    __version_test__ = "v1.0.7"
    assert __version_test__ == "v1.0.7"

    assert re.match(r"^v1.0.7?.+$", __version_test__)  # nosec
    assert re.match(r"^v\d{1,5}\.\d{1,5}\.\d{1,5}$", __version_test__)  # nosec
