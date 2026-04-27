#!/usr/bin/env python3
import logging
import os
import re
import sys
import traceback
from typing import (  # for annotation purposes only; Any,; Dict,; List,; Iterator,; Pattern,; noqa: E501
    Tuple,
)

import certifi
import click
import urllib3
from colorama import init
from jira import JIRA
from jira.exceptions import JIRAError
from termcolor import colored

# from get_jira.get_auth import match_auth

http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where(),
)

# use Colorama to make Termcolor work on Windows too
init()


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
    confirmation_prompt=True,
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
@click.option(
    "-f",
    "--fail",
    is_flag=True,
    default=False,
    help="Fail if no issue JIRA found",
)
def cli(
    current_message: str,
    branch: str,
    fail=True,
    user=None,
    password=None,
    verbose=False,
) -> str:
    """Simple program that match jira. From hooks directory : Try
    python -m get_jira.get_jira BMT-13403 feature/TEST-13403 --verbose
    python -m get_jira.get_jira TEST feature/TEST-13403 --verbose
    python -m get_jira.get_jira 'Test message' feature/TEST-99999 --verbose
    """

    logger.info("Collecting JIRA")

    if verbose:
        click.echo(branch)
        click.echo(user)
        # click.echo(password)
        click.echo(fail)
        click.echo(verbose)

    basic_auth = match_auth(user, password)  # noqa: F821

    msg = get_msg(
        current_message=current_message,
        branch=branch,
        basic_auth=basic_auth,
        verbose=verbose,
        fail=fail,
    )

    print(colored("Message: {}".format(msg[0]), "magenta"))

    return msg


def get_msg(
    current_message: str,
    branch: str,
    basic_auth: Tuple[str, str] = ("", ""),
    verbose=True,
    fail=True,
) -> Tuple[str, str]:
    issue = match_issue(
        branch=branch,
        verbose=verbose,
    )

    required_message = ""

    # Test that message has not already been populated
    if issue not in current_message:
        required_message = match_jira(
            issue=issue,
            basic_auth=basic_auth,
            verbose=verbose,
        )

        # Appending current message
        required_message = "{} : {}".format(required_message, current_message)
    else:
        if verbose:
            print(
                colored(
                    "Issue number already detected in message: {}".format(
                        required_message,
                    ),
                    "yellow",
                ),
            )

    return required_message, issue


def match_issue(branch: str, verbose=False, fail=True) -> str:
    """
    Extract JIRA issue from branch name.
    
    Supports branch naming patterns like:
    - feature/PROJ-123
    - bugfix/TEST-456
    - feat/ABC-789
    """
    issue = "UNKNOWN"

    try:
        # Matches any unique issue code in branch name
        pattern = re.compile(
            r"(^feature|^feat|^bugfix|^fix|^docs|^style|^refactor|^perf|^test|^chore)\/([A-Z]{2,10}-[0-9]+)",
        )
        match = re.search(pattern, branch)
        if match:
            issue = match.group(2)  # Extract issue code
            if verbose:
                print(colored("Issue number detected : {}.".format(issue), "green"))
        else:
            # Try to extract from branch name even without prefix
            pattern = re.compile(r"([A-Z]{2,10}-[0-9]+)")
            match = re.search(pattern, branch)
            if match:
                issue = match.group(1)
                if verbose:
                    print(colored("Issue number detected : {}.".format(issue), "green"))

    except Exception:
        if verbose:
            traceback.print_exc()
        print(
            colored(
                "Please set a valid JIRA",
                "red",
            ),
        )
        if fail:
            sys.exit(2)

    return issue


def match_issue_from_message(message: str, verbose=False) -> str:
    """
    Extract JIRA issue from commit message.
    
    Looks for pattern like PROJ-123, TEST-456, etc. anywhere in the message.
    
    Args:
        message: The commit message
        verbose: If True, print debug information
        
    Returns:
        The JIRA issue if found, "UNKNOWN" otherwise
    """
    issue = "UNKNOWN"
    
    try:
        # Match JIRA pattern: 2-10 uppercase letters, dash, numbers
        pattern = re.compile(r"([A-Z]{2,10}-[0-9]+)")
        match = re.search(pattern, message)
        
        if match:
            issue = match.group(1)
            if verbose:
                print(colored(f"Issue number detected in message: {issue}", "green"))
    except Exception:
        if verbose:
            traceback.print_exc()
    
    return issue


def get_jira_url() -> str:
    try:
        url = os.environ.get("JIRA_URL")

        if not url:
            server = "localhost/jira"
            url = "https://%s" % server

    except KeyError:
        print(
            colored(
                "Please set the environment variable JIRA_URL",
                "red",
            ),
        )
        sys.exit(3)

    return url


def get_certificat_path() -> str:
    try:
        certificat_path = os.environ.get("JIRA_CERT_PATH")

        if not certificat_path:
            certificat_path = "/etc/ssl/certs/ca-certificates.crt"

    except KeyError:
        print(
            colored(
                "Please set the environment variable JIRA_CERT_PATH",
                "red",
            ),
        )
        sys.exit(3)

    return certificat_path


def match_jira(
    issue: str,
    basic_auth: Tuple[str, str] = ("", ""),
    verbose=False,
) -> str:
    # WORKAROUND below in case certificate is not install on workstation
    urllib3.disable_warnings()

    required_message = ""

    try:
        # print(colored('URL : {}.'.format(get_jira_url()), 'red'))

        options = {
            "server": get_jira_url(),
            "verify": False,
            # 'verify': True,
            # 'client_cert': get_certificat_path(),
        }

        jira = JIRA(options, basic_auth=basic_auth)

        issue_to_check = jira.issue(issue)
        status = "{}".format(issue_to_check.fields.status).strip().lower()

        issuetype = "{}".format(issue_to_check.fields.issuetype.name).strip().lower()

        # versions = jira.project_versions('TEST')
        # print(
        #     colored(
        #         'Versions : {}'.format(
        #             versions,
        #         ), 'magenta',
        #     ),
        # )
        # [v.name for v in reversed(versions)]

        if verbose:
            print(
                colored(
                    "Project key : {}".format(
                        issue_to_check.fields.project.key,
                    ),
                    "magenta",
                ),
            )
            print(
                colored(
                    "Issue Type : {}".format(
                        issuetype,
                    ),
                    "magenta",
                ),
            )  # 'Story'
            print(
                colored(
                    "Status : {}".format(
                        status,
                    ),
                    "magenta",
                ),
            )  # 'Story'
            print(
                colored(
                    "Reporter : {}".format(
                        issue_to_check.fields.reporter.displayName,
                    ),
                    "magenta",
                ),
            )

        statustocheck = ["closed", "done"]

        if any(sta in status for sta in statustocheck):
            print(
                colored(
                    "Status : {}".format(
                        status,
                    ),
                    "red",
                ),
            )
            sys.exit(3)

        required_message = "{} : {}".format(
            issue,
            issue_to_check.fields.issuetype.name,
        )
    except JIRAError as e:
        if verbose:
            traceback.print_exc()
        if e.status_code == 404:
            print(
                colored(
                    "{}".format(
                        e.text,
                    ),
                    "red",
                ),
            )
        if e.status_code == 401:
            print(
                colored(
                    "Login to JIRA failed. Check your username and password {}".format(
                        options,
                    ),
                    "red",
                ),
            )
    except Exception:
        if verbose:
            traceback.print_exc()
        print(
            colored(
                "Oops!  JIRA is failing. Switch to manual... {}".format(
                    issue,
                ),
                "red",
            ),
        )
        if jira:
            sys.exit(2)

    return required_message


logger = logging.getLogger("hooks.get_jira.get_jira")

if __name__ == "__main__":
    cli(None)
