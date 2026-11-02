#!/usr/bin/env python3
"""
Simple JIRA / GitHub issue commit message validator.

This module validates that commit messages contain JIRA ticket or GitHub issue
references without requiring any API access. It's designed to be used as a commit-msg hook.
"""

import argparse
import re
import sys
from typing import Optional

from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()


def extract_jira_ticket(message: str, pattern: Optional[str] = None) -> Optional[str]:
    """
    Extract JIRA ticket from commit message.

    Args:
        message: The commit message to check
        pattern: Optional custom regex pattern for JIRA tickets

    Returns:
        The JIRA ticket if found, None otherwise
    """
    if pattern is None:
        # Default pattern: PROJECT-123 format (2-10 uppercase letters, dash, numbers)
        pattern = r"[A-Z]{2,10}-[0-9]+"

    match = re.search(pattern, message)
    return match.group(0) if match else None


# #123, owner/repo#123 or GH-123 (GitHub autolinks all three)
GITHUB_PATTERN = r"(?:[\w.-]+/[\w.-]+)?#[0-9]+\b|\bGH-[0-9]+\b"
JIRA_PATTERN = r"[A-Z]{2,10}-[0-9]+"
TRACKER_PATTERNS = {
    "jira": JIRA_PATTERN,
    "github": GITHUB_PATTERN,
    "any": f"{JIRA_PATTERN}|{GITHUB_PATTERN}",
}


def extract_issue(message: str, tracker: str = "jira", pattern: Optional[str] = None) -> Optional[str]:
    """Return the first JIRA ticket or GitHub issue reference, ignoring git comment lines."""
    text = "\n".join(line for line in message.splitlines() if not line.startswith("#"))
    return extract_jira_ticket(text, pattern or TRACKER_PATTERNS[tracker])


def is_special_commit(message: str) -> bool:
    """
    Check if this is a special commit that should skip JIRA validation.

    Args:
        message: The commit message to check

    Returns:
        True if this is a merge, revert, or other special commit
    """
    first_line = message.strip().split("\n")[0] if message else ""

    # Skip merge commits
    if first_line.startswith("Merge "):
        return True

    # Skip revert commits
    if first_line.startswith("Revert "):
        return True

    # Skip fixup and squash commits
    if first_line.startswith(("fixup! ", "squash! ")):
        return True

    return False


def validate_commit_message(
    commit_msg_filepath: str,
    pattern: Optional[str] = None,
    verbose: bool = False,
    tracker: str = "jira",
) -> bool:
    """
    Validate that commit message contains a JIRA ticket or a GitHub issue.

    Args:
        commit_msg_filepath: Path to the commit message file
        pattern: Optional custom regex pattern, overrides the tracker one
        verbose: If True, print detailed information
        tracker: "jira", "github" or "any"

    Returns:
        True if valid, False otherwise
    """
    try:
        with open(commit_msg_filepath) as f:
            message = f.read()

        if not message.strip():
            print(colored("Empty commit message", "yellow"))
            return False

        # Check if this is a special commit that should be skipped
        if is_special_commit(message):
            print(colored("Special commit detected (merge/revert/fixup/squash), skipping issue check", "green"))
            return True

        label = {"jira": "JIRA ticket", "github": "GitHub issue", "any": "JIRA ticket or GitHub issue"}[tracker]
        ticket = extract_issue(message, tracker, pattern)

        if ticket:
            print(colored(f"✓ {label} found: {ticket}", "green"))
            return True
        else:
            print(colored(f"✗ Error: No {label} found in commit message", "red"))
            first_line = message.strip().split("\n")[0]
            print(colored(f"Commit message subject: {first_line}", "yellow"))
            pattern_display = pattern or TRACKER_PATTERNS[tracker]
            print(colored(f"Expected pattern: {pattern_display}", "yellow"))
            print()
            print(colored("Examples of valid commit messages:", "cyan"))
            if tracker != "github":
                print(colored("  PROJ-123: Add new feature", "green"))
                print(colored("  [ABC-789] Update documentation", "green"))
            if tracker != "jira":
                print(colored("  fix: crash on empty config (#42)", "green"))
                print(colored("  GH-42 Fix critical bug", "green"))
                print(colored("  feat: add login, closes owner/repo#42", "green"))
            print()
            print(colored(f"Tip: Reference a {label} in your commit message", "cyan"))
            return False

    except FileNotFoundError:
        print(colored(f"Error: Commit message file not found: {commit_msg_filepath}", "red"))
        return False
    except Exception as e:
        print(colored(f"Error validating commit message: {e}", "red"))
        return False


def main():
    """Main entry point for the JIRA commit message validator."""

    parser = argparse.ArgumentParser(
        description="Validate that commit messages contain JIRA ticket or GitHub issue references",
    )
    parser.add_argument(
        "commit_msg_file",
        help="Path to the commit message file",
    )
    parser.add_argument(
        "--pattern",
        help="Custom regex pattern for JIRA tickets (default: [A-Z]{2,10}-[0-9]+)",
        default=None,
    )
    parser.add_argument(
        "--tracker",
        choices=sorted(TRACKER_PATTERNS),
        default="jira",
        help="Issue tracker to require: jira (default), github (#123, owner/repo#123, GH-123) or any",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    is_valid = validate_commit_message(
        args.commit_msg_file,
        pattern=args.pattern,
        verbose=args.verbose,
        tracker=args.tracker,
    )

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
