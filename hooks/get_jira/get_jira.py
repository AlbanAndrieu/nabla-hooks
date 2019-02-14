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
@click.argument('branch', type=str)
@click.option('-u', '--user', required=False, envvar='JIRA_USER', help='JIRA user')  # noqa: ignore=E501
@click.option('-p', '--password', required=False, envvar='JIRA_PASSWORD', help='JIRA password')  # noqa: ignore=E501
@click.option('-v', '--verbose', is_flag=True, default=False, help='Switch between INFO and DEBUG logging modes')  # noqa: ignore=E501
def cli(branch: str, user=None, password=None, verbose=False) -> str:
    """Simple program that match jira. From hooks directory : Try python -m get_jira.get_jira feature/BMT-13403 -v"""

    logger.info('Collecting JIRA')

    if verbose:
        click.echo(branch)
        click.echo(user)
        click.echo(password)
        click.echo(verbose)

    basic_auth = match_auth(user, password)

    return match_jira(branch=branch, basic_auth=basic_auth, verbose=verbose)


def match_jira(branch: str, basic_auth: Tuple[str, str] = ('', ''), verbose=False) -> str:

    # WORKAROUND below in case certificate is not install on workstation
    urllib3.disable_warnings()

    issue = 'UNKNOWN'

    try:
        # Matches any unique issue code
        pattern = re.compile(r'(^feature|^bugfix)\/([A-Z]{3,5}-[0-9]+)')
        issue = re.search(pattern, branch).group(2)  # Extract issue code
        if verbose:
            print(colored('Issue number detected : {}.'.format(issue), 'green'))

        server = 'almtools.misys.global.ad/jira'
        options = {
            'server': 'https://%s' % server,
            'verify': '/etc/ssl/certs/UK1VSWCERT01-CA-5.crt',
        }

        jira = JIRA(options, basic_auth=basic_auth)

        issue_to_check = jira.issue(issue)
        print(issue_to_check.fields.project.key)             # 'JRA'
        print(issue_to_check.fields.issuetype.name)          # 'New Feature'
        print(issue_to_check.fields.reporter.displayName)

        required_message = '%s : %s by %s' % (
            issue_to_check, issue_to_check.fields.issuetype.name, issue_to_check.fields.reporter.displayName,
        )
    except JIRAError as e:
        if verbose:
            traceback.print_exc()
        # sys.stderr.write(
        #    "Failed to create Jira object.  Message: \"%s\".\n" % (e.text),
        # )
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
