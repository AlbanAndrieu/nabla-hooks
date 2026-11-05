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
from termcolor import colored

from .get_auth import jira_auth

# use Colorama to make Termcolor work on Windows too
init()

JIRA_KEY = re.compile(r"[A-Z]{2,10}-[0-9]+")
SYSTEM_CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"
# Fields printed or checked below: fetching only these keeps the response small.
ISSUE_FIELDS = "status,issuetype,project,reporter"


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
        user=user,
        password=password,
        verbose=verbose,
    )

    print(colored("Message: {}".format(msg[0]), "magenta"))

    return msg


def get_msg(
    current_message: str,
    branch: str,
    user=None,
    password=None,
    verbose=True,
) -> Tuple[str, str]:
    """Prefix the message with '<issue> : <issue type>', unless the issue is already in it."""
    issue = match_issue(branch=branch, verbose=verbose)

    # Before any credential lookup: no password prompt when there is nothing to query.
    if issue in current_message:
        if verbose:
            print(colored("Issue number already detected in message: {}".format(issue), "yellow"))
        return "", issue

    prefix = match_jira(issue=issue, user=user, password=password, verbose=verbose)
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


def get_timeout() -> float:
    """Seconds before giving up on JIRA, so an unreachable server never blocks a commit for long."""
    return float(os.environ.get("JIRA_TIMEOUT") or 10)


def get_certificat_path() -> str:
    """CA bundle used to check the JIRA certificate: JIRA_CERT_PATH (e.g. an internal CA), else the system one."""
    default = SYSTEM_CA_BUNDLE if os.path.exists(SYSTEM_CA_BUNDLE) else certifi.where()
    return os.environ.get("JIRA_CERT_PATH") or default


def match_jira(
    issue: str,
    user=None,
    password=None,
    verbose=False,
) -> str:
    """Return '<issue> : <issue type>', exit 3 if the issue is closed, "" if JIRA refuses the request."""
    # Imported here: the jira client costs ~170 ms, paid only when JIRA is queried.
    from jira import JIRA  # noqa: PLC0415
    from jira.exceptions import JIRAError  # noqa: PLC0415

    url = get_jira_url()
    if not url.startswith("https://"):
        print(colored("JIRA_URL must start with https:// so credentials are not sent in clear: {}".format(url), "red"))
        return ""

    auth = jira_auth(user=user, password=password, verbose=verbose)
    try:
        # No server-info call and no retries: one HTTP request per commit, bounded by the timeout.
        jira = JIRA(
            options={"server": url, "verify": get_certificat_path()},
            get_server_info=False,
            max_retries=0,
            timeout=get_timeout(),
            **auth,
        )
        fields = jira.issue(issue, fields=ISSUE_FIELDS).fields
    except JIRAError as e:
        if verbose:
            traceback.print_exc()
        if e.status_code == 401:
            print(colored("Login to JIRA failed. Check your credentials (JIRA_USER and JIRA_API_TOKEN, or JIRA_PAT) for {}".format(url), "red"))
        else:
            print(colored("{}".format(e.text), "red"))
        return ""
    except Exception as error:
        # Offline, timeout or TLS error: like Linear and GitHub, never block the commit.
        if verbose:
            traceback.print_exc()
        print(colored("Could not check JIRA issue {}, message left unchanged: {!r}".format(issue, error), "yellow"))
        return ""

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
