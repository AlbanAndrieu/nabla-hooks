#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ['alban.andrieu@finastra.com']

import re
import sys
import logging
import click
import traceback
import urllib3
from get_jira.get_auth import match_auth
from jira import JIRA
from jira.exceptions import JIRAError

from colorama import init
from termcolor import colored

from typing import (  # for annotation purposes only
    #    Any,
    #    Dict,
    #    List,
    Tuple,
    #    Iterator,
    #    Pattern,
)

# use Colorama to make Termcolor work on Windows too
init()


@click.command()
@click.argument('current_message', type=str)
@click.argument('branch', type=str)
@click.option('-u', '--user', required=False, envvar='JIRA_USER', help='JIRA user')  # noqa: ignore=E501
@click.option('-p', '--password', required=False, prompt=False, hide_input=True, confirmation_prompt=True, envvar='JIRA_PASSWORD', help='JIRA password')  # noqa: ignore=E501
@click.option('-v', '--verbose', is_flag=True, default=False, help='Switch between INFO and DEBUG logging modes')  # noqa: ignore=E501
def cli(current_message: str, branch: str, user=None, password=None, verbose=False) -> str:
    """Simple program that match jira. From hooks directory : Try
    python -m get_jira.get_jira BMT-13403 feature/BMT-13403 --verbose
    python -m get_jira.get_jira TEST feature/BMT-13403 --verbose
    """

    logger.info('Collecting JIRA')

    if verbose:
        click.echo(branch)
        click.echo(user)
        # click.echo(password)
        click.echo(verbose)

    basic_auth = match_auth(user, password)

    msg = get_msg(current_message=current_message, branch=branch, basic_auth=basic_auth, verbose=verbose)

    print(colored('Message: {}'.format(msg[0]), 'magenta'))

    return msg


def get_msg(current_message: str, branch: str, basic_auth: Tuple[str, str] = ('', ''), verbose=True) -> Tuple[str, str]:

    issue = match_issue(
        branch=branch, verbose=verbose,
    )

    required_message = ''

    # Test that message has not already been populated
    if issue not in current_message:
        required_message = match_jira(
            issue=issue, basic_auth=basic_auth, verbose=verbose,
        )

        # Appending current message
        required_message = '{} : {}'.format(required_message, current_message)
    else:
        if verbose:
            print(colored('Issue number already detected in message: {}'.format(required_message), 'yellow'))

    return required_message, issue


def match_issue(branch: str, verbose=False) -> str:

    issue = 'UNKNOWN'

    # Matches any unique issue code
    pattern = re.compile(r'(^feature|^bugfix)\/([A-Z]{3,5}-[0-9]+)')
    issue = re.search(pattern, branch).group(2)  # Extract issue code
    if verbose:
        print(colored('Issue number detected : {}.'.format(issue), 'green'))

    return issue


def match_jira(issue: str, basic_auth: Tuple[str, str] = ('', ''), verbose=False) -> str:

    # WORKAROUND below in case certificate is not install on workstation
    urllib3.disable_warnings()

    required_message = ''

    try:

        server = 'almtools.misys.global.ad/jira'
        options = {
            'server': 'https://%s' % server,
            'verify': '/etc/ssl/certs/UK1VSWCERT01-CA-5.crt',
        }

        jira = JIRA(options, basic_auth=basic_auth)

        issue_to_check = jira.issue(issue)
        status = '{}'.format(issue_to_check.fields.status).strip().lower()

        if verbose:
            print(
                colored(
                    'Project key : {}'.format(
                        issue_to_check.fields.project.key,
                    ), 'magenta',
                ),
            )
            print(
                colored(
                    'Issue Type : {}'.format(
                        issue_to_check.fields.issuetype.name,
                    ), 'magenta',
                ),
            )               # 'Story'
            print(
                colored(
                    'Status : {}'.format(
                        status,
                    ), 'magenta',
                ),
            )               # 'Story'
            print(
                colored(
                    'Reporter : {}'.format(
                        issue_to_check.fields.reporter.displayName,
                    ), 'magenta',
                ),
            )

        statustocheck = ['closed', 'done']

        if any(sta in status for sta in statustocheck):
            print(
                colored(
                    'Status : {}'.format(
                        status,
                    ), 'red',
                ),
            )
            sys.exit(3)

        required_message = '{} : {}'.format(
            issue, issue_to_check.fields.issuetype.name,
        )
    except JIRAError as e:
        if verbose:
            traceback.print_exc()
        if e.status_code == 404:
            print(
                colored(
                    '{}'.format(
                        e.text,
                    ), 'red',
                ),
            )
        if e.status_code == 401:
            print(
                colored(
                    'Login to JIRA failed. Check your username and password {}'.format(
                        options,
                    ), 'red',
                ),
            )
    except Exception as e:  # noqa: ignore=E722
        if verbose:
            traceback.print_exc()
        print(
            colored(
                'Oops!  JIRA is failing. Switch to manual... {}'.format(
                    issue,
                ), 'red',
            ),
        )
        sys.exit(2)

    return required_message


logger = logging.getLogger('hooks.get_jira.get_jira')

if __name__ == '__main__':
    cli(None)
