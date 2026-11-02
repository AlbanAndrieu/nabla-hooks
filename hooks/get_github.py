#!/usr/bin/env python3
"""GitHub issue support: read the issue number from the branch and check it with the gh CLI."""

import json
import re
import subprocess  # nosec B404
import sys
from typing import Optional, Tuple

from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

__all__ = ["get_msg", "match_issue"]

# feature/123-add-login, fix/GH-42, issue-7, 123-hotfix
BRANCH_PATTERN = re.compile(r"(?:^|/)(?:GH-|gh-|issue-|issues/)?([0-9]+)(?=[-_]|$)")


def match_issue(branch: str) -> Optional[str]:
    """Return the GitHub issue number found in the branch name, or None."""
    match = BRANCH_PATTERN.search(branch)
    return match.group(1) if match else None


def get_msg(current_message: str, branch: str, verbose: bool = False) -> Tuple[str, str]:
    """Prefix the message with GH-<number>, after checking the issue is still open."""
    issue = match_issue(branch)
    if issue is None or re.search(rf"(?:#|GH-){issue}\b", current_message):
        return "", issue or ""

    try:
        output = subprocess.run(  # nosec B603 B607
            ["gh", "issue", "view", issue, "--json", "title,state"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout
        details = json.loads(output)
    except (OSError, subprocess.SubprocessError, ValueError) as error:
        # Unknown number (e.g. fix/2026-10-31), offline or gh logged out: never add a wrong reference.
        print(colored(f"Could not check GitHub issue #{issue}, message left unchanged: {error}", "yellow"))
        return "", issue

    if details.get("state") == "CLOSED":
        print(colored(f"GitHub issue #{issue} is closed: {details.get('title', '')}", "red"))
        sys.exit(3)
    if verbose:
        print(colored(f"GitHub issue #{issue}: {details.get('title', '')}", "magenta"))

    # "GH-" rather than "#": git strips lines starting with "#" as comments.
    return f"GH-{issue} : {current_message}", issue
