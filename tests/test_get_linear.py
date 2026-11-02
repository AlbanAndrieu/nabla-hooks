"""Tests for hooks/get_linear.py module."""

import io
import json
import sys
import urllib.error
from unittest.mock import patch

import pytest

sys.path.insert(0, "hooks")

from hooks.get_linear import get_msg, match_issue


@pytest.mark.parametrize(
    ("branch", "expected"),
    [
        ("alban/eng-123-add-login", "ENG-123"),
        ("feature/ENG-42", "ENG-42"),
        ("eng-7", "ENG-7"),
        ("feature/123-add-login", None),
        ("release/1.2.0", None),
        ("feature/v2-ui", None),
    ],
)
def test_match_issue(branch, expected):
    assert match_issue(branch) == expected


def _linear(issue):
    return io.BytesIO(json.dumps({"data": {"issue": issue}}).encode())


@pytest.fixture
def api_key(monkeypatch):
    monkeypatch.setenv("LINEAR_API_KEY", "lin_api_test")


@patch("hooks.get_linear.urllib.request.urlopen", return_value=_linear({"title": "Login", "state": {"type": "started"}}))
def test_get_msg_open_issue(mock_urlopen, api_key):
    assert get_msg("Add login", "alban/eng-42-login") == ("ENG-42 : Add login", "ENG-42")
    request = mock_urlopen.call_args.args[0]
    assert request.get_header("Authorization") == "lin_api_test"
    assert json.loads(request.data)["variables"] == {"id": "ENG-42"}


@pytest.mark.parametrize("state", ["completed", "canceled"])
def test_get_msg_closed_issue_fails(api_key, state):
    with patch("hooks.get_linear.urllib.request.urlopen", return_value=_linear({"title": "Login", "state": {"type": state}})):
        with pytest.raises(SystemExit) as excinfo:
            get_msg("Add login", "alban/eng-42-login")
    assert excinfo.value.code == 3


@patch("hooks.get_linear.urllib.request.urlopen", return_value=_linear(None))
def test_get_msg_unknown_issue_leaves_message(mock_urlopen, api_key):
    assert get_msg("Add login", "alban/eng-42-login") == ("", "ENG-42")


@patch("hooks.get_linear.urllib.request.urlopen", side_effect=urllib.error.URLError("offline"))
def test_get_msg_offline_leaves_message(mock_urlopen, api_key):
    assert get_msg("Add login", "alban/eng-42-login") == ("", "ENG-42")


@patch("hooks.get_linear.urllib.request.urlopen")
def test_get_msg_without_api_key(mock_urlopen, monkeypatch):
    monkeypatch.delenv("LINEAR_API_KEY", raising=False)
    assert get_msg("Add login", "alban/eng-42-login") == ("", "ENG-42")
    mock_urlopen.assert_not_called()


@patch("hooks.get_linear.urllib.request.urlopen")
def test_get_msg_already_referenced(mock_urlopen, api_key):
    assert get_msg("eng-42 : Add login", "alban/eng-42-login") == ("", "ENG-42")
    mock_urlopen.assert_not_called()
