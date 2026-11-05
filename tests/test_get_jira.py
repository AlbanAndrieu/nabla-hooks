"""Tests for hooks/get_jira/get_jira.py."""

from types import SimpleNamespace
from unittest.mock import patch

import pytest
from jira.exceptions import JIRAError

from hooks.get_jira.get_jira import ISSUE_FIELDS, get_certificat_path, get_msg, match_issue, match_jira


@pytest.fixture(autouse=True)
def jira_env(monkeypatch):
    """A bearer token, so no test reads the developer's own credentials or prompts."""
    monkeypatch.setenv("JIRA_PAT", "test-pat")
    monkeypatch.setenv("JIRA_URL", "https://jira.example.com")


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


@patch("jira.JIRA")
def test_match_jira_verifies_tls(mock_jira, monkeypatch):
    monkeypatch.setenv("JIRA_CERT_PATH", "/path/to/ca.pem")
    mock_jira.return_value.issue.return_value = fake_issue()

    assert match_jira("PROJ-1") == "PROJ-1 : Story"
    assert mock_jira.call_args.kwargs["options"]["verify"] == "/path/to/ca.pem"


@patch("jira.JIRA")
def test_match_jira_single_bounded_request(mock_jira, monkeypatch):
    monkeypatch.setenv("JIRA_TIMEOUT", "3")
    mock_jira.return_value.issue.return_value = fake_issue()

    match_jira("PROJ-1")

    kwargs = mock_jira.call_args.kwargs
    assert kwargs["get_server_info"] is False
    assert kwargs["max_retries"] == 0
    assert kwargs["timeout"] == 3.0
    assert kwargs["token_auth"] == "test-pat"
    mock_jira.return_value.issue.assert_called_once_with("PROJ-1", fields=ISSUE_FIELDS)


@patch("jira.JIRA")
def test_match_jira_refuses_plain_http(mock_jira, monkeypatch):
    monkeypatch.setenv("JIRA_URL", "http://jira.example.com")

    assert match_jira("PROJ-1") == ""
    mock_jira.assert_not_called()


@patch("jira.JIRA")
def test_match_jira_unreachable_keeps_message(mock_jira):
    mock_jira.return_value.issue.side_effect = ConnectionError("timed out")

    assert match_jira("PROJ-1") == ""


@patch("jira.JIRA")
def test_match_jira_closed_issue_exits_3(mock_jira):
    mock_jira.return_value.issue.return_value = fake_issue(status="Done")

    with pytest.raises(SystemExit) as excinfo:
        match_jira("PROJ-1")
    assert excinfo.value.code == 3


@patch("jira.JIRA")
def test_get_msg_keeps_message_when_jira_refuses(mock_jira):
    mock_jira.return_value.issue.side_effect = JIRAError(status_code=404, text="Issue does not exist")

    assert get_msg("Add login", "feature/PROJ-1") == ("", "PROJ-1")


@patch("jira.JIRA")
def test_get_msg_issue_already_in_message(mock_jira, monkeypatch):
    monkeypatch.delenv("JIRA_PAT")
    with patch("getpass.getpass") as mock_getpass:
        assert get_msg("PROJ-1 : Add login", "feature/PROJ-1") == ("", "PROJ-1")
    mock_jira.assert_not_called()
    mock_getpass.assert_not_called()


def test_get_certificat_path_default(monkeypatch):
    monkeypatch.delenv("JIRA_CERT_PATH", raising=False)
    assert get_certificat_path().endswith(".crt") or get_certificat_path().endswith(".pem")
