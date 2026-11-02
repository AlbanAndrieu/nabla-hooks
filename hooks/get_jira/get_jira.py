#!/usr/bin/env python3
import logging
import os
import re
import sys
import traceback
from typing import Tuple

import certifi
import click
from colorama import init
from jira import JIRA
from jira.exceptions import JIRAError
from termcolor import colored

from .get_auth import match_auth

# use Colorama to make Termcolor work on Windows too
init()

JIRA_KEY = re.compile(r"[A-Z]{2,10}-[0-9]+")
SYSTEM_CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"


@click.command()
@click.argument("current_message", type=str)
@click.argument("branch", type=str)
@click.option(
    "-u",
    "--user",
    required=False,
    envvar="JIRA_USER",
    help="JIRA user",
)
@click.option(
    "-p",
    "--password",
    required=False,
    prompt=False,
    hide_input=True,
    envvar="JIRA_PASSWORD",
    help="JIRA password",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Switch between INFO and DEBUG logging modes",
)
def cli(
    current_message: str,
    branch: str,
    user=None,
    password=None,
    verbose=False,
) -> Tuple[str, str]:
    """Simple program that match jira. From hooks directory : Try
    python -m get_jira.get_jira 'Test message' feature/TEST-99999 --verbose
    """

    logger.info("Collecting JIRA")

    msg = get_msg(
        current_message=current_message,
        branch=branch,
        basic_auth=match_auth(user, password),
        verbose=verbose,
    )

    print(colored("Message: {}".format(msg[0]), "magenta"))

    return msg


def get_msg(
    current_message: str,
    branch: str,
    basic_auth: Tuple[str, str] = ("", ""),
    verbose=True,
) -> Tuple[str, str]:
    """Prefix the message with '<issue> : <issue type>', unless the issue is already in it."""
    issue = match_issue(branch=branch, verbose=verbose)

    if issue in current_message:
        if verbose:
            print(colored("Issue number already detected in message: {}".format(issue), "yellow"))
        return "", issue

    prefix = match_jira(issue=issue, basic_auth=basic_auth, verbose=verbose)
    # JIRA refused the request: keep the message rather than writing " : <message>".
    return ("{} : {}".format(prefix, current_message) if prefix else ""), issue


def match_issue(branch: str, verbose=False) -> str:
    """
    Extract JIRA issue from branch name, "UNKNOWN" if there is none.

    Supports branch naming patterns like:
    - feature/PROJ-123
    - bugfix/TEST-456
    - PROJ-789-short-description
    """
    match = JIRA_KEY.search(branch)
    if not match:
        return "UNKNOWN"
    if verbose:
        print(colored("Issue number detected : {}.".format(match.group()), "green"))
    return match.group()


def get_jira_url() -> str:
    return os.environ.get("JIRA_URL") or "https://localhost/jira"


def get_certificat_path() -> str:
    """CA bundle used to check the JIRA certificate: JIRA_CERT_PATH (e.g. an internal CA), else the system one."""
    default = SYSTEM_CA_BUNDLE if os.path.exists(SYSTEM_CA_BUNDLE) else certifi.where()
    return os.environ.get("JIRA_CERT_PATH") or default


def match_jira(
    issue: str,
    basic_auth: Tuple[str, str] = ("", ""),
    verbose=False,
) -> str:
    """Return '<issue> : <issue type>', exit 3 if the issue is closed, "" if JIRA refuses the request."""
    try:
        jira = JIRA({"server": get_jira_url(), "verify": get_certificat_path()}, basic_auth=basic_auth)
        fields = jira.issue(issue).fields
    except JIRAError as e:
        if verbose:
            traceback.print_exc()
        if e.status_code == 401:
            print(colored("Login to JIRA failed. Check your username and password for {}".format(get_jira_url()), "red"))
        else:
            print(colored("{}".format(e.text), "red"))
        return ""
    except Exception:
        if verbose:
            traceback.print_exc()
        print(colored("Oops!  JIRA is failing. Switch to manual... {}".format(issue), "red"))
        sys.exit(2)

    status = "{}".format(fields.status).strip().lower()

    if verbose:
        print(
            colored(
                "Project key : {}\nIssue Type : {}\nStatus : {}\nReporter : {}".format(
                    fields.project.key,
                    fields.issuetype.name,
                    status,
                    fields.reporter.displayName,
                ),
                "magenta",
            ),
        )

    if any(closed in status for closed in ("closed", "done")):
        print(colored("Status : {}".format(status), "red"))
        sys.exit(3)

    return "{} : {}".format(issue, fields.issuetype.name)


logger = logging.getLogger("hooks.get_jira.get_jira")

if __name__ == "__main__":
    cli(None)
