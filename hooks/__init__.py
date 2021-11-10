#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This module allow to customize git hooks.
"""
# import hooks.get_jira  # noqa: F401
import uuid

from hooks._version import get_versions
# from . import _version

name = 'hooks'

signing_uuid = uuid.UUID('dd34b62f-9ed5-597e-85a2-c15d48ed6832')
__version__ = get_versions()['version']
del get_versions

# __version__ = 'v1.0.2'
# __version__ = _version.get_versions()['version']

__all__ = ('__version__', 'signing_uuid')
