#!/usr/bin/env python3
"""Linear issue support: read the issue key from the branch and check it with the Linear API."""

import json
import os
import re
import sys
import urllib.request
from typing import Optional, Tuple

from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

__all__ = ["get_msg", "match_issue"]

API_URL = "https://api.linear.app/graphql"
QUERY = "query($id: String!) { issue(id: $id) { title state { type } } }"
CLOSED_STATES = ("completed", "canceled")

# alban/eng-123-add-login (Linear default branch name), feature/ENG-123
BRANCH_PATTERN = re.compile(r"(?:^|/)([a-zA-Z]{2,10}-[0-9]+)(?=[-_/]|$)")


def match_issue(branch: str) -> Optional[str]:
    """Return the Linear issue key (ENG-123) found in the branch name, or None."""
    match = BRANCH_PATTERN.search(branch)
    return match.group(1).upper() if match else None


def get_msg(current_message: str, branch: str, verbose: bool = False) -> Tuple[str, str]:
    """Prefix the message with the Linear key, after checking the issue is still open."""
    issue = match_issue(branch)
    if issue is None or re.search(rf"\b{issue}\b", current_message, re.IGNORECASE):
        return "", issue or ""

    api_key = os.environ.get("LINEAR_API_KEY")
    if not api_key:
        print(colored(f"LINEAR_API_KEY is not set, Linear issue {issue} not checked, message left unchanged", "yellow"))
        return "", issue

    request = urllib.request.Request(
        API_URL,
        data=json.dumps({"query": QUERY, "variables": {"id": issue}}).encode(),
        headers={"Authorization": api_key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:  # nosec B310
            details = json.load(response)["data"]["issue"]
        state = details["state"]["type"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        # Unknown key (Linear answers data: null), offline or bad key: never add a wrong reference.
        print(colored(f"Could not check Linear issue {issue}, message left unchanged: {error!r}", "yellow"))
        return "", issue

    if state in CLOSED_STATES:
        print(colored(f"Linear issue {issue} is {state}: {details.get('title', '')}", "red"))
        sys.exit(3)
    if verbose:
        print(colored(f"Linear issue {issue}: {details.get('title', '')}", "magenta"))

    return f"{issue} : {current_message}", issue
