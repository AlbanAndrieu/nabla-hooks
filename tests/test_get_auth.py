"""Tests for hooks/get_jira/get_auth.py module."""

import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, "hooks")

from hooks.get_jira.get_auth import get_password, get_user, match_auth


class TestGetAuth:
    """Test cases for get_auth module."""

    def test_get_user_with_provided_user(self):
        """Test get_user returns the provided user."""
        user = get_user(user="testuser", verbose=False)
        assert user == "testuser"

    def test_get_user_from_jira_user_env(self):
        """Test get_user retrieves from JIRA_USER environment variable."""
        with patch.dict(os.environ, {"JIRA_USER": "envuser"}):
            user = get_user(user=None, verbose=False)
            assert user == "envuser"

    def test_get_user_from_git_username_env(self):
        """Test get_user retrieves from GIT_USERNAME as fallback."""
        with patch.dict(os.environ, {"GIT_USERNAME": "gituser"}, clear=True):
            user = get_user(user=None, verbose=False)
            assert user == "gituser"

    def test_get_user_exits_when_no_user_provided(self):
        """Test get_user exits with code 3 when no user is found."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(SystemExit) as excinfo:
                get_user(user=None, verbose=False)
            assert excinfo.value.code == 3

    def test_get_password_with_provided_password(self):
        """Test get_password returns the provided password."""
        password = get_password(password="testpass", verbose=False)
        assert password == "testpass"

    def test_get_password_from_jira_password_env(self):
        """Test get_password retrieves from JIRA_PASSWORD environment variable."""
        with patch.dict(os.environ, {"JIRA_PASSWORD": "envpass"}):
            password = get_password(password=None, verbose=False)
            assert password == "envpass"

    def test_get_password_from_git_assword_env(self):
        """Test get_password retrieves from GIT_ASSWORD as fallback.
        
        Note: The environment variable is intentionally named GIT_ASSWORD (typo in original code).
        """
        with patch.dict(os.environ, {"GIT_ASSWORD": "gitpass"}, clear=True):
            password = get_password(password=None, verbose=False)
            assert password == "gitpass"

    def test_get_password_exits_when_no_password_provided(self):
        """Test get_password exits with code 3 when no password is found."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("getpass.getpass", return_value=None):
                with pytest.raises(SystemExit) as excinfo:
                    get_password(password=None, verbose=False)
                assert excinfo.value.code == 3

    def test_match_auth_success(self):
        """Test match_auth returns tuple of user and password."""
        with patch.dict(
            os.environ, {"JIRA_USER": "testuser", "JIRA_PASSWORD": "testpass"}
        ):
            basic_auth = match_auth(user=None, password=None, verbose=False)
            assert basic_auth == ("testuser", "testpass")

    def test_match_auth_with_provided_credentials(self):
        """Test match_auth with explicitly provided credentials."""
        basic_auth = match_auth(user="myuser", password="mypass", verbose=False)
        assert basic_auth == ("myuser", "mypass")

    def test_match_auth_verbose_mode(self):
        """Test match_auth in verbose mode."""
        with patch.dict(
            os.environ, {"JIRA_USER": "verboseuser", "JIRA_PASSWORD": "verbosepass"}
        ):
            basic_auth = match_auth(user=None, password=None, verbose=True)
            assert basic_auth == ("verboseuser", "verbosepass")
