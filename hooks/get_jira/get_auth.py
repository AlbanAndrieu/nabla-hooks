#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import getpass
import logging
import os
import sys
from typing import (  # for annotation purposes only
    #    Any,
    #    Dict,
    #    List,
    Tuple,
    #    Iterator,
    #    Pattern,
)

import click
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()


@click.command()
@click.option('-u', '--user', required=False, envvar='JIRA_USER', help='JIRA user')  # noqa: ignore=E501
@click.option('-p', '--password', required=False, prompt=True, hide_input=True, confirmation_prompt=True, envvar='JIRA_PASSWORD', help='JIRA password')  # noqa: ignore=E501
@click.option('-v', '--verbose', is_flag=True, default=False, help='Switch between INFO and DEBUG logging modes')  # noqa: ignore=E501
def cli(user=None, password=None, verbose=False) -> Tuple[str, str]:
    """Simple program that match jira. From hooks directory : Try python -m get_jira.get_auth -u aandrieu -p XXXX --verbose"""

    logger.info('Collecting authentifcation')

    return match_auth(user, password, verbose)


def get_user(user=None, verbose=False) -> str:

    try:

        if not user:
            if verbose:
                print(
                    colored(
                        'User is empty, using JIRA_USER environement variable.', 'yellow',
                    ),
                )
            user = os.environ.get('JIRA_USER')
            if not user:
                user = os.environ.get('GIT_USERNAME')

        if not user:
            print(colored('User cannot be empty : {}.'.format(user), 'red'))
            sys.exit(3)

    except KeyError:
        print(
            colored(
                'Please set the environment variable JIRA_USER or GIT_USERNAME', 'red',
            ),
        )
        sys.exit(3)

    # print(colored('User : {}.'.format(user), 'red'))

    return user


def get_password(password=None, verbose=False) -> str:

    try:

        if not password:
            if verbose:
                print(
                    colored(
                        'Password is empty, using JIRA_PASSWORD environement variable', 'yellow',
                    ),
                )
            password = os.environ.get('JIRA_PASSWORD')
            if not password:
                password = os.environ.get('GIT_ASSWORD')
            if not password:
                password = getpass.getpass()

            # TODO password should be crypted

        if not password:
            print(colored('Password cannot be empty : {}.'.format(password), 'red'))
            sys.exit(3)

    except KeyError:
        print(
            colored(
                'Please set the environment variable JIRA_PASSWORD or GIT_PASSWORD', 'red',
            ),
        )
        sys.exit(3)

    # print(colored('Password : {}.'.format(password), 'red'))

    return password


def match_auth(user=None, password=None, verbose=False) -> Tuple[str, str]:

    if verbose:
        logger.setLevel(logging.DEBUG)
        click.echo(user)
        # click.echo(password)
        click.echo(verbose)

    user = get_user(user=user, verbose=verbose)

    password = get_password(password=password, verbose=verbose)

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
