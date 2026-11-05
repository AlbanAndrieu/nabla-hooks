#!/usr/bin/env python3
import getpass
import logging
import os
import sys
from typing import (  # for annotation purposes only; Any,; Dict,; List,; Iterator,; Pattern,; noqa: E501
    Tuple,
)

import click
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()


@click.command()
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
    prompt=True,
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
def cli(user=None, password=None, verbose=False) -> Tuple[str, str]:
    """Simple program that match jira. From hooks directory : Try python -m get_jira.get_auth -u aandrieu --verbose"""

    logger.info("Collecting authentifcation")

    return match_auth(user, password, verbose)


def get_user(user=None, verbose=False) -> str:
    try:
        if not user:
            if verbose:
                print(
                    colored(
                        "User is empty, using JIRA_USER environement variable.",
                        "yellow",
                    ),
                )
            user = os.environ.get("JIRA_USER")
            if not user:
                user = os.environ.get("GIT_USERNAME")

        if not user:
            print(colored("User cannot be empty : {}.".format(user), "red"))
            sys.exit(3)

    except KeyError:
        print(
            colored(
                "Please set the environment variable JIRA_USER or GIT_USERNAME",
                "red",
            ),
        )
        sys.exit(3)

    # print(colored('User : {}.'.format(user), 'red'))

    return user


KEYRING_SERVICE = "nabla-hooks-jira"


def get_keyring_password(user=None) -> str:
    """Secret stored with `keyring set nabla-hooks-jira <user>`, "" when there is none or no keyring backend."""
    if not user:
        return ""
    try:
        import keyring  # noqa: PLC0415 - lazy: only needed when no token is in the environment

        return keyring.get_password(KEYRING_SERVICE, user) or ""
    except Exception:  # no backend (headless, CI): fall back to the prompt
        return ""


def get_password(password=None, verbose=False, user=None) -> str:
    try:
        if not password:
            if verbose:
                print(
                    colored(
                        "Password is empty, using JIRA_API_TOKEN, JIRA_PASSWORD or the {} keyring".format(KEYRING_SERVICE),
                        "yellow",
                    ),
                )
            password = os.environ.get("JIRA_API_TOKEN") or os.environ.get("JIRA_PASSWORD") or os.environ.get("GIT_PASSWORD") or get_keyring_password(user)
            if not password:
                try:
                    password = getpass.getpass("JIRA password or API token: ")
                except (EOFError, OSError):  # no terminal (GUI client, CI)
                    password = None

        if not password:
            print(colored("Password cannot be empty : {}.".format(password), "red"))
            sys.exit(3)

    except KeyError:
        print(
            colored(
                "Please set the environment variable JIRA_API_TOKEN, JIRA_PASSWORD or GIT_PASSWORD",
                "red",
            ),
        )
        sys.exit(3)

    return password


def match_auth(user=None, password=None, verbose=False) -> Tuple[str, str]:
    if verbose:
        logger.setLevel(logging.DEBUG)
        click.echo(user)
        # click.echo(password)
        click.echo(verbose)

    user = get_user(user=user, verbose=verbose)

    password = get_password(password=password, verbose=verbose, user=user)

    # Never print the tuple: it holds the password.
    return (user, password)


def jira_auth(user=None, password=None, verbose=False) -> dict:
    """JIRA() auth keyword: JIRA_PAT as a bearer token (Server/Data Center), else basic auth (Cloud: email + API token)."""
    pat = os.environ.get("JIRA_PAT")
    if pat:
        return {"token_auth": pat}
    return {"basic_auth": match_auth(user=user, password=password, verbose=verbose)}


logger = logging.getLogger("hooks.get_jira.get_auth")
logger.setLevel(logging.INFO)
stdoutlog = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutlog)

if __name__ == "__main__":
    cli(None)
