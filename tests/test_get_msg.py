"""Tests for hooks/get_msg.py module."""

import os
import sys
from unittest.mock import mock_open, patch

import pytest

sys.path.insert(0, "hooks")

from hooks.get_msg import match_msg


class TestGetMsg:
    """Test cases for get_msg module."""

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="Test commit message")
    @patch("os.path.exists")
    def test_match_msg_non_feature_branch(
        self,
        mock_exists,
        mock_file,
        mock_check_output,
    ):
        """Test match_msg on a non-feature branch returns original message."""
        # Setup
        mock_check_output.return_value = b"main"
        mock_exists.return_value = True

        # Execute
        result = match_msg(
            commit_msg_filepath="/tmp/COMMIT_EDITMSG",
            commit_type="",
            jira=False,
            verbose=False,
        )

        # Assert - on non-feature branch, should not modify message
        # The result should be empty because no feature/bugfix branch pattern matched
        assert result == ""

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="Test message")
    @patch("os.path.exists")
    def test_match_msg_feature_branch_no_jira(
        self,
        mock_exists,
        mock_file,
        mock_check_output,
    ):
        """Without JIRA nor a GitHub issue number, the message is kept as is."""
        mock_check_output.return_value = b"feature/TEST-123"
        mock_exists.return_value = True

        result = match_msg(
            commit_msg_filepath="/tmp/COMMIT_EDITMSG",
            commit_type="message",
            jira=False,
            verbose=False,
        )

        assert result == "Test message"

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="Add login")
    @patch("os.path.exists")
    @patch("hooks.get_msg.get_github.get_msg")
    @patch("hooks.get_msg.get_jira.get_jira.get_msg")
    def test_match_msg_github_branch(
        self,
        mock_jira_get_msg,
        mock_github_get_msg,
        mock_exists,
        mock_file,
        mock_check_output,
    ):
        """A feature/<number> branch uses GitHub, never JIRA."""
        mock_check_output.return_value = b"feature/42-add-login"
        mock_exists.return_value = True
        mock_github_get_msg.return_value = ("GH-42 : Add login", "42")

        result = match_msg(commit_msg_filepath="/tmp/COMMIT_EDITMSG", commit_type="message")

        assert result == "GH-42 : Add login"
        mock_jira_get_msg.assert_not_called()

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="Add login")
    @patch("os.path.exists")
    @patch("hooks.get_msg.get_github.get_msg")
    def test_match_msg_closed_issue_keeps_exit_code(
        self,
        mock_github_get_msg,
        mock_exists,
        mock_file,
        mock_check_output,
    ):
        """A closed issue exits 3 through match_msg, not the generic 2."""
        mock_check_output.return_value = b"feature/42-add-login"
        mock_exists.return_value = True
        mock_github_get_msg.side_effect = SystemExit(3)

        with pytest.raises(SystemExit) as excinfo:
            match_msg(commit_msg_filepath="/tmp/COMMIT_EDITMSG", commit_type="message")
        assert excinfo.value.code == 3

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("os.path.exists")
    def test_match_msg_empty_message(self, mock_exists, mock_file, mock_check_output):
        """Test match_msg with empty commit message."""
        # Setup
        mock_check_output.return_value = b"main"
        mock_exists.return_value = True

        # Execute
        result = match_msg(
            commit_msg_filepath="/tmp/COMMIT_EDITMSG",
            commit_type="",
            jira=False,
            verbose=False,
        )

        # Assert
        assert result == ""

    @patch("hooks.get_msg.check_output")
    @patch("os.path.exists")
    def test_match_msg_file_not_exists(self, mock_exists, mock_check_output):
        """Test match_msg when commit message file doesn't exist."""
        # Setup
        mock_check_output.return_value = b"main"
        mock_exists.return_value = False

        # Execute
        result = match_msg(
            commit_msg_filepath="/tmp/COMMIT_EDITMSG",
            commit_type="",
            jira=False,
            verbose=False,
        )

        # Assert - should return empty string when file doesn't exist
        assert result == ""

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="Feature update")
    @patch("os.path.exists")
    @patch("hooks.get_msg.get_jira.get_auth.match_auth")
    @patch("hooks.get_msg.get_jira.get_jira.get_msg")
    def test_match_msg_feature_branch_with_jira(
        self,
        mock_jira_get_msg,
        mock_match_auth,
        mock_exists,
        mock_file,
        mock_check_output,
    ):
        """Test match_msg on feature branch with JIRA enabled."""
        # Setup
        mock_check_output.return_value = b"feature/TEST-456"
        mock_exists.return_value = True
        mock_match_auth.return_value = ("testuser", "testpass")
        mock_jira_get_msg.return_value = ("TEST-456: Updated feature message",)

        # Execute
        with patch.dict(
            os.environ,
            {"JIRA_USER": "testuser", "JIRA_PASSWORD": "testpass"},
        ):
            result = match_msg(
                commit_msg_filepath="/tmp/COMMIT_EDITMSG",
                commit_type="message",
                jira=True,
                user="testuser",
                password="testpass",
                verbose=False,
            )

        # Assert
        assert result == "TEST-456: Updated feature message"
        mock_jira_get_msg.assert_called_once()

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="Bugfix commit")
    @patch("os.path.exists")
    def test_match_msg_bugfix_branch(self, mock_exists, mock_file, mock_check_output):
        """Test match_msg on bugfix branch without JIRA keeps the message."""
        mock_check_output.return_value = b"bugfix/BUG-789"
        mock_exists.return_value = True

        result = match_msg(
            commit_msg_filepath="/tmp/COMMIT_EDITMSG",
            commit_type="message",
            jira=False,
            verbose=False,
        )

        assert result == "Bugfix commit"

    @patch("hooks.get_msg.check_output")
    @patch("builtins.open", new_callable=mock_open, read_data="Test")
    @patch("os.path.exists")
    def test_match_msg_verbose_mode(self, mock_exists, mock_file, mock_check_output):
        """Test match_msg in verbose mode."""
        # Setup
        mock_check_output.return_value = b"main"
        mock_exists.return_value = True

        # Execute - verbose should just enable debug logging
        result = match_msg(
            commit_msg_filepath="/tmp/COMMIT_EDITMSG",
            commit_type="",
            jira=False,
            verbose=True,
        )

        # Assert
        assert result == ""
