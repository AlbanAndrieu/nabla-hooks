"""Tests for prepare-commit-msg hook with oco/opencommit compatibility."""
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add hooks to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))


def test_prepare_commit_msg_with_existing_message():
    """Test that prepare_commit_msg allows existing messages (from oco/opencommit)."""
    # Import after path is set
    from prepare_commit_msg import prepare_commit_msg

    # Create a temporary file with a commit message (as if from oco)
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("feat: add new feature\n\nThis is a detailed description.")
        temp_file = f.name

    try:
        # Mock subprocess.run for cz check
        with patch("subprocess.run") as mock_run:
            # Simulate cz check returning success
            mock_run.return_value = MagicMock(returncode=0)

            result = prepare_commit_msg(temp_file)

            # Should return 0 (success) and not call cz commit
            assert result == 0
            # Should only call cz check, not cz commit
            assert mock_run.call_count == 1
            assert mock_run.call_args[0][0] == ["cz", "check", "--commit-msg-file", temp_file]
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_prepare_commit_msg_with_existing_message_invalid():
    """Test that prepare_commit_msg allows existing messages even if invalid with cz."""
    from prepare_commit_msg import prepare_commit_msg

    # Create a temporary file with a commit message that might not pass cz check
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("This is a custom commit message from oco")
        temp_file = f.name

    try:
        with patch("subprocess.run") as mock_run:
            # Simulate cz check returning failure
            mock_run.return_value = MagicMock(returncode=1)

            # Mock print to avoid output
            with patch("builtins.print"):
                result = prepare_commit_msg(temp_file)

            # Should still return 0 (allow the message)
            assert result == 0
            # Should only call cz check
            assert mock_run.call_count == 1
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_prepare_commit_msg_with_empty_message():
    """Test that prepare_commit_msg generates message when file is empty."""
    from prepare_commit_msg import prepare_commit_msg

    # Create an empty temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("")
        temp_file = f.name

    try:
        with patch("subprocess.run") as mock_run, patch("builtins.input") as mock_input:
            # Mock input to say no to backup
            mock_input.return_value = "n"
            # Simulate cz commit success
            mock_run.return_value = MagicMock(returncode=0)

            # Mock Path.is_file to return False (no backup file)
            with patch.object(Path, "is_file", return_value=False):
                result = prepare_commit_msg(temp_file)

            # Should call cz commit to generate message
            assert result == 0
            # Should call cz commit
            cz_commit_called = any(
                "cz" in str(call[0][0]) and "commit" in str(call[0][0])
                for call in mock_run.call_args_list
            )
            assert cz_commit_called
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_prepare_commit_msg_with_comments_only():
    """Test that prepare_commit_msg treats comment-only files as empty."""
    from prepare_commit_msg import prepare_commit_msg

    # Create a file with only comments
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("# Please enter the commit message\n# Lines starting with '#' are comments\n")
        temp_file = f.name

    try:
        with patch("subprocess.run") as mock_run, patch("builtins.input") as mock_input:
            mock_input.return_value = "n"
            mock_run.return_value = MagicMock(returncode=0)

            with patch.object(Path, "is_file", return_value=False):
                result = prepare_commit_msg(temp_file)

            # Should generate message (treat as empty)
            assert result == 0
            # Should call cz commit
            cz_commit_called = any(
                "cz" in str(call[0][0]) and "commit" in str(call[0][0])
                for call in mock_run.call_args_list
            )
            assert cz_commit_called
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
