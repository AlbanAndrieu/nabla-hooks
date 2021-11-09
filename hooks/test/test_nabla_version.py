# -*- coding: utf-8 -*-
import re

from hooks import __version__


def test_version():
    # assert __version__ == '1.0.2'
    assert re.match(r'^v1.0.2.+$', __version__)  # nosec
