#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ['alban.andrieu@finastra.com']

import os
import sys
import logging
import click

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
@click.option('-u', '--user', required=False, envvar='JIRA_USER', help='JIRA user')  # noqa: ignore=E501
@click.option('-p', '--password', required=False, envvar='JIRA_PASSWORD', help='JIRA password')  # noqa: ignore=E501
@click.option('-v', '--verbose', is_flag=True, default=False, help='Switch between INFO and DEBUG logging modes')  # noqa: ignore=E501
def cli(user=None, password=None, verbose=False) -> Tuple[str, str]:
    """Simple program that match jira. From hooks directory : Try python -m get_jira.get_auth -u aandrieu -p XXXX -v"""

    logger.info('Collecting authentifcation')

    return match_auth(user, password, verbose)


def match_auth(user=None, password=None, verbose=False) -> Tuple[str, str]:

    if verbose:
        logger.setLevel(logging.DEBUG)
        click.echo(user)
        click.echo(password)
        click.echo(verbose)

    try:
        os.environ['JIRA_USER']
        os.environ['JIRA_PASSWORD']
    except KeyError:
        print(colored(
            'Please set the environment variable JIRA_USER and JIRA_PASSWORD', 'red',
        ))
        sys.exit(3)

    if not user:
        if verbose:
            print(
                colored(
                    'User is empty, using JIRA_USER environement variable.', 'yellow',
                ),
            )
        user = os.environ.get('JIRA_USER', 'TODO')

    if not user:
        print(colored('User cannot be empty : {}.'.format(user), 'red'))
        sys.exit(3)
    if not password:
        if verbose:
            print(colored(
                'Password is empty, using JIRA_PASSWORD environement variable', 'yellow',
            ))
        password = os.environ.get('JIRA_PASSWORD', 'TODO')
    if not password:
        print(colored('Password cannot be empty : {}.'.format(password), 'red'))
        sys.exit(3)
    basic_auth = (user, password)

    if not basic_auth:
        print(colored('Authentification cannot be empty : {}.'.format(basic_auth), 'red'))
        sys.exit(3)
    else:
        if verbose:
            print(basic_auth)
    return basic_auth


logger = logging.getLogger('hooks.get_jira.get_auth')
logger.setLevel(logging.INFO)
stdoutlog = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutlog)

if __name__ == '__main__':
    cli(None)
