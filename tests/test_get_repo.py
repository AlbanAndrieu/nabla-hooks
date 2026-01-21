"""Tests for hooks/get_repo.py module."""

import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "hooks")

from hooks.get_repo import (
    _get_org_and_name_from_remote,
    _get_sha,
    _get_url,
)


class TestGetRepo:
    """Test cases for get_repo module."""

    def test_get_sha(self):
        """Test _get_sha returns correct SHA."""
        # Create mock git repo
        mock_repo = MagicMock()
        mock_repo.head.object.hexsha = "abc123def456"

        sha = _get_sha(mock_repo)

        assert sha == "abc123def456"

    def test_get_url(self):
        """Test _get_url returns correct URL."""
        # Create mock git repo
        mock_repo = MagicMock()
        mock_repo.remotes.origin.url = "https://github.com/AlbanAndrieu/nabla-hooks.git"

        url = _get_url(mock_repo)

        assert url == "https://github.com/AlbanAndrieu/nabla-hooks.git"

    def test_get_org_and_name_from_remote_with_git_extension(self):
        """Test parsing org and repo name from URL with .git extension."""
        url = "https://github.com/AlbanAndrieu/nabla-hooks.git"

        owner, name = _get_org_and_name_from_remote(url)

        assert owner == "AlbanAndrieu"
        assert name == "nabla-hooks"

    def test_get_org_and_name_from_remote_without_git_extension(self):
        """Test parsing org and repo name from URL without .git extension."""
        url = "https://github.com/AlbanAndrieu/nabla-hooks"

        owner, name = _get_org_and_name_from_remote(url)

        assert owner == "AlbanAndrieu"
        assert name == "nabla-hooks"

    def test_get_org_and_name_from_remote_ssh_url(self):
        """Test parsing org and repo name from SSH URL."""
        url = "git@github.com:AlbanAndrieu/nabla-hooks.git"

        owner, name = _get_org_and_name_from_remote(url)

        assert owner == "AlbanAndrieu"
        assert name == "nabla-hooks"

    def test_get_org_and_name_from_remote_verbose(self, capsys):
        """Test parsing with verbose output."""
        url = "https://github.com/TestOrg/test-repo.git"

        owner, name = _get_org_and_name_from_remote(url, verbose=True)

        captured = capsys.readouterr()
        assert 'Repo owner: "TestOrg"' in captured.out
        assert 'Repo name: "test-repo"' in captured.out
        assert owner == "TestOrg"
        assert name == "test-repo"
