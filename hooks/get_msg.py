#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ['alban.andrieu@finastra.com']

import re
import sys
import logging
import click
import get_jira.get_auth
import get_jira.get_jira
from subprocess import check_output

from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()


@click.command()
@click.argument('commit_msg_filepath', type=click.Path(exists=True))
@click.option('-u', '--user', required=False, envvar='JIRA_USER', help='JIRA user')  # noqa: ignore=E501
@click.option('-p', '--password', required=False, envvar='JIRA_PASSWORD', help='JIRA password')  # noqa: ignore=E501
@click.option('-v', '--verbose', is_flag=True, default=False, help='Switch between INFO and DEBUG logging modes')  # noqa: ignore=E501
def cli(commit_msg_filepath, user=None, password=None, verbose=False):
    """Simple program that check a commit message. Try ./get_msg.py '../.git/COMMIT_EDITMSG'"""

    logger.info('Collecting branch')

    if verbose:
        click.echo(click.format_filename(commit_msg_filepath))
        click.echo(user)
        click.echo(password)
        click.echo(verbose)

    match_msg(commit_msg_filepath, user, password, verbose)


def match_msg(commit_msg_filepath, user=None, password=None, verbose=False) -> str:

    if verbose:
        logger.setLevel(logging.DEBUG)

    basic_auth = get_jira.get_auth.match_auth(
        user=user, password=password, verbose=verbose,
    )

    # Figure out which branch we're on
    branch = check_output([
        'git', 'symbolic-ref', '--short',
        'HEAD',
    ]).strip().decode('utf-8')

    logger.debug(r"msg: On branch '{}'".format(branch))
    regex = re.compile('^feature|^bugfix')

    issue = 'UNKNOWN'
    required_message = '%s' % issue

    # Populate the commit message with the issue #, if there is one
    if re.match(regex, branch):
        print(colored(
            "Oh hey, it's an issue branch : {}.".format(
                branch,
            ), 'green',
        ))

        required_message = get_jira.get_jira.match_jira(
            branch=branch, basic_auth=basic_auth, verbose=verbose,
        )

        with open(commit_msg_filepath, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write('%s : %s' % (required_message, content))

    return required_message


logger = logging.getLogger('hooks.get_msg')
logger.setLevel(logging.INFO)
stdoutlog = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutlog)

if __name__ == '__main__':
    cli(None)
