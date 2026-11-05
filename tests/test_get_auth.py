"""Tests for hooks/get_jira/get_auth.py module."""

import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, "hooks")

from hooks.get_jira.get_auth import KEYRING_SERVICE, get_password, get_user, jira_auth, match_auth


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
        with patch.dict(os.environ, {"JIRA_PASSWORD": "envpass"}, clear=True):
            password = get_password(password=None, verbose=False)
            assert password == "envpass"

    def test_get_password_prefers_api_token(self):
        """JIRA_API_TOKEN (JIRA Cloud) wins over JIRA_PASSWORD."""
        with patch.dict(os.environ, {"JIRA_API_TOKEN": "token", "JIRA_PASSWORD": "envpass"}, clear=True):
            assert get_password(password=None, verbose=False) == "token"

    def test_get_password_from_git_password_env(self):
        """Test get_password retrieves from GIT_PASSWORD as fallback."""
        with patch.dict(os.environ, {"GIT_PASSWORD": "gitpass"}, clear=True):
            password = get_password(password=None, verbose=False)
            assert password == "gitpass"

    def test_get_password_from_keyring(self):
        """The keyring is read for the user when no secret is in the environment."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("keyring.get_password", return_value="ringpass") as mock_keyring:
                assert get_password(password=None, verbose=False, user="me") == "ringpass"
            mock_keyring.assert_called_once_with(KEYRING_SERVICE, "me")

    def test_get_password_keyring_failure_falls_back_to_prompt(self):
        """A missing keyring backend falls back to the prompt."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("keyring.get_password", side_effect=RuntimeError("no backend")):
                with patch("getpass.getpass", return_value="typed"):
                    assert get_password(password=None, verbose=False, user="me") == "typed"

    def test_get_password_exits_when_no_password_provided(self):
        """Test get_password exits with code 3 when no password is found."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("getpass.getpass", return_value=None):
                with pytest.raises(SystemExit) as excinfo:
                    get_password(password=None, verbose=False)
                assert excinfo.value.code == 3

    def test_get_password_exits_without_terminal(self):
        """No terminal to prompt on (GUI client, CI): exit 3 instead of a traceback."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("getpass.getpass", side_effect=EOFError):
                with pytest.raises(SystemExit) as excinfo:
                    get_password(password=None, verbose=False)
                assert excinfo.value.code == 3

    def test_jira_auth_uses_pat_as_bearer(self):
        """JIRA_PAT is sent as a bearer token and no password is asked."""
        with patch.dict(os.environ, {"JIRA_PAT": "pat"}, clear=True):
            with patch("getpass.getpass") as mock_getpass:
                assert jira_auth() == {"token_auth": "pat"}
            mock_getpass.assert_not_called()

    def test_jira_auth_basic(self):
        """Without JIRA_PAT, basic auth with user and API token."""
        with patch.dict(os.environ, {"JIRA_USER": "me@example.com", "JIRA_API_TOKEN": "token"}, clear=True):
            assert jira_auth() == {"basic_auth": ("me@example.com", "token")}

    def test_match_auth_success(self):
        """Test match_auth returns tuple of user and password."""
        with patch.dict(
            os.environ,
            {"JIRA_USER": "testuser", "JIRA_PASSWORD": "testpass"},
            clear=True,
        ):
            basic_auth = match_auth(user=None, password=None, verbose=False)
            assert basic_auth == ("testuser", "testpass")

    def test_match_auth_with_provided_credentials(self):
        """Test match_auth with explicitly provided credentials."""
        basic_auth = match_auth(user="myuser", password="mypass", verbose=False)
        assert basic_auth == ("myuser", "mypass")

    def test_match_auth_verbose_mode(self, capsys):
        """Test match_auth in verbose mode never prints the password."""
        with patch.dict(
            os.environ,
            {"JIRA_USER": "verboseuser", "JIRA_PASSWORD": "verbosepass"},
            clear=True,
        ):
            basic_auth = match_auth(user=None, password=None, verbose=True)
            assert basic_auth == ("verboseuser", "verbosepass")
        assert "verbosepass" not in capsys.readouterr().out
