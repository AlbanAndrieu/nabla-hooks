#!/usr/bin/env python3
import logging
import os
import re
import sys
import traceback
from subprocess import check_output  # nosec

import click
import get_github
import get_jira.get_auth
import get_jira.get_jira
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

__all__ = ["match_msg"]

ISSUE_BRANCH = re.compile("^feature|^feat|^bugfix|^fix")


@click.command()
@click.argument("commit_msg_filepath", type=click.Path(exists=False))
@click.argument("commit_type", type=str, default="")  # message for prepare-commit-msg
@click.option(
    "-j",
    "--jira",
    is_flag=True,
    default=True,
    help="Jira check",
)
@click.option(
    "--github/--no-github",
    default=True,
    envvar="NABLA_GITHUB_ISSUES",
    help="GitHub issue check (branch feature/123-xxx), needs the gh CLI",
)
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
    # get_auth asks for it only when JIRA is actually queried.
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
    commit_msg_filepath,
    commit_type: str = "",
    jira=True,
    github=True,
    user=None,
    password=None,
    verbose=False,
):
    """
    Configures git hook commit message using CLI.

    :param str commit_msg_filepath: **required** *"./.git/COMMIT_EDITMSG"*, -
                    path of the file where the message is stored by git. If not provided, defaults to hostname

    :param str commit_msg_filepath: **default** *""*, -
                    Type of the message given by git. If not provided, defaults to empty

    :returns: Msg

    :example:

    .. code-block:: bash

             echo "TEST" > ../.git/COMMIT_EDITMSG
             ./get_msg.py '../.git/COMMIT_EDITMSG' 'message'

    """

    logger.info("Collecting branch")

    if verbose:
        click.echo(click.format_filename(commit_msg_filepath))
        click.echo(jira)
        click.echo(user)
        # click.echo(password)
        click.echo(verbose)

    return match_msg(
        commit_msg_filepath=commit_msg_filepath,
        commit_type=commit_type,
        jira=jira,
        github=github,
        user=user,
        password=password,
        verbose=verbose,
    )


def issue_message(current_message: str, branch: str, jira=True, github=True, user=None, password=None, verbose=False) -> str:
    """Message prefixed with the branch issue, "" when there is nothing to add."""
    # A JIRA key wins; otherwise a bare number is a GitHub issue.
    if jira and get_jira.get_jira.match_issue(branch) != "UNKNOWN":
        return get_jira.get_jira.get_msg(
            current_message=current_message,
            branch=branch,
            basic_auth=get_jira.get_auth.match_auth(user=user, password=password, verbose=verbose),
            verbose=verbose,
        )[0]
    if github:
        return get_github.get_msg(current_message=current_message, branch=branch, verbose=verbose)[0]
    return ""


def match_msg(
    commit_msg_filepath: str,
    commit_type: str = "",
    jira=True,
    github=True,
    user=None,
    password=None,
    verbose=False,
) -> str:
    """
    Configures git hook commit message.

    :param str commit_msg_filepath: **required** *"./.git/COMMIT_EDITMSG"*, -
                    path of the file where the message is stored by git. If not provided, defaults to hostname

    :param str commit_msg_filepath: **default** *""*, -
                    Type of the message given by git. If not provided, defaults to empty

    :returns: Msg
    """

    if verbose:
        logger.setLevel(logging.DEBUG)

    try:
        branch = check_output(["/usr/bin/git", "symbolic-ref", "--short", "HEAD"]).strip().decode("utf-8")
        logger.debug("msg: On branch '{}'".format(branch))

        filename = os.path.expanduser(commit_msg_filepath)
        if not os.path.exists(filename):
            return ""

        with open(filename) as f:
            current_message = f.read()

        if not current_message:
            print(colored("Current message is empty.", "red"))
        elif verbose:
            print(colored("Message before is : {}".format(current_message), "yellow"))

        if not ISSUE_BRANCH.match(branch):
            return ""

        if "message" in commit_type:
            print(colored("Oh hey, it's an issue branch : {}.".format(branch), "green"))

        required_message = issue_message(current_message, branch, jira, github, user, password, verbose) or current_message

        if verbose:
            print(colored("Message after is : {}".format(required_message), "yellow"))

        with open(filename, "w") as f:
            f.write(required_message)

        return required_message

    # Not BaseException: the issue checks exit 3 on a closed issue and that code must reach git.
    except Exception:
        traceback.print_exc()
        sys.exit(2)


logger = logging.getLogger("hooks.get_msg")
logger.setLevel(logging.INFO)
stdoutlog = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutlog)

if __name__ == "__main__":
    cli(None)
