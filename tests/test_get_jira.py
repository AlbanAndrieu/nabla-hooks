"""Tests for hooks/get_jira/get_jira.py."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from jira.exceptions import JIRAError

from hooks.get_jira.get_jira import get_certificat_path, get_msg, match_issue, match_jira


@pytest.mark.parametrize(
    ("branch", "expected"),
    [
        ("feature/PROJ-123", "PROJ-123"),
        ("bugfix/TEST-456-crash", "TEST-456"),
        ("ABC-789-no-prefix", "ABC-789"),
        ("feature/42-github", "UNKNOWN"),
        ("main", "UNKNOWN"),
    ],
)
def test_match_issue(branch, expected):
    assert match_issue(branch) == expected


def fake_issue(status="In Progress"):
    fields = SimpleNamespace(
        status=status,
        issuetype=SimpleNamespace(name="Story"),
        project=SimpleNamespace(key="PROJ"),
        reporter=SimpleNamespace(displayName="Someone"),
    )
    return SimpleNamespace(fields=fields)


@patch("hooks.get_jira.get_jira.JIRA")
def test_match_jira_verifies_tls(mock_jira, monkeypatch):
    monkeypatch.setenv("JIRA_CERT_PATH", "/path/to/ca.pem")
    mock_jira.return_value.issue.return_value = fake_issue()

    assert match_jira("PROJ-1") == "PROJ-1 : Story"
    assert mock_jira.call_args.args[0]["verify"] == "/path/to/ca.pem"


@patch("hooks.get_jira.get_jira.JIRA")
def test_match_jira_closed_issue_exits_3(mock_jira):
    mock_jira.return_value.issue.return_value = fake_issue(status="Done")

    with pytest.raises(SystemExit) as excinfo:
        match_jira("PROJ-1")
    assert excinfo.value.code == 3


@patch("hooks.get_jira.get_jira.JIRA")
def test_get_msg_keeps_message_when_jira_refuses(mock_jira):
    mock_jira.return_value.issue.side_effect = JIRAError(status_code=404, text="Issue does not exist")

    assert get_msg("Add login", "feature/PROJ-1") == ("", "PROJ-1")


def test_get_msg_issue_already_in_message():
    with patch("hooks.get_jira.get_jira.JIRA", MagicMock()) as mock_jira:
        assert get_msg("PROJ-1 : Add login", "feature/PROJ-1") == ("", "PROJ-1")
    mock_jira.assert_not_called()


def test_get_certificat_path_default(monkeypatch):
    monkeypatch.delenv("JIRA_CERT_PATH", raising=False)
    assert get_certificat_path().endswith(".crt") or get_certificat_path().endswith(".pem")
