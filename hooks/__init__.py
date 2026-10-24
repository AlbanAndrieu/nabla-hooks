#!/usr/bin/env python
"""
This module allow to customize git hooks.
"""

# import hooks.get_jira
import uuid
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

name = "hooks"

signing_uuid = uuid.UUID("dd34b62f-9ed5-597e-85a2-c15d48ed6832")

try:
    __version__ = version("nabla-hooks")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = ("__version__", "signing_uuid")
