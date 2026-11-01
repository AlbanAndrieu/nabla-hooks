"""Tests for hooks/get_github.py module."""

import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, "hooks")

from hooks.get_github import get_msg, match_issue


@pytest.mark.parametrize(
    ("branch", "expected"),
    [
        ("feature/123-add-login", "123"),
        ("fix/GH-42", "42"),
        ("issue-7-crash", "7"),
        ("feat/issues/9", "9"),
        ("feature/TEST-123", None),
        ("release/1.2.0", None),
        ("feature/v2-ui", None),
    ],
)
def test_match_issue(branch, expected):
    assert match_issue(branch) == expected


def _gh(stdout):
    return MagicMock(stdout=stdout)


@patch("hooks.get_github.subprocess.run", return_value=_gh('{"title": "Login", "state": "OPEN"}'))
def test_get_msg_open_issue(mock_run):
    assert get_msg("Add login", "feature/42-login") == ("GH-42 : Add login", "42")
    assert mock_run.call_args.args[0][:4] == ["gh", "issue", "view", "42"]


@patch("hooks.get_github.subprocess.run", return_value=_gh('{"title": "Login", "state": "CLOSED"}'))
def test_get_msg_closed_issue_fails(mock_run):
    with pytest.raises(SystemExit) as excinfo:
        get_msg("Add login", "feature/42-login")
    assert excinfo.value.code == 3


@patch("hooks.get_github.subprocess.run", side_effect=subprocess.CalledProcessError(1, "gh"))
def test_get_msg_unknown_issue_leaves_message(mock_run):
    assert get_msg("Add login", "fix/2026-10-31") == ("", "2026")


@patch("hooks.get_github.subprocess.run")
@pytest.mark.parametrize("message", ["GH-42 : Add login", "Add login (#42)"])
def test_get_msg_already_referenced(mock_run, message):
    assert get_msg(message, "feature/42-login") == ("", "42")
    mock_run.assert_not_called()


@patch("hooks.get_github.subprocess.run")
def test_get_msg_no_issue(mock_run):
    assert get_msg("Add login", "feature/login") == ("", "")
    mock_run.assert_not_called()
