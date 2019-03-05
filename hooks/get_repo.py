#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys

import click
import git
from colorama import init
from giturlparse import parse

# use Colorama to make Termcolor work on Windows too
init()


@click.command()
@click.option('-u', '--user', required=False, envvar='JIRA_USER', help='JIRA user')  # noqa: ignore=E501
@click.option('-p', '--password', required=False, prompt=True, hide_input=True, confirmation_prompt=True, envvar='JIRA_PASSWORD', help='JIRA password')  # noqa: ignore=E501
@click.option('-v', '--verbose', is_flag=True, default=False, help='Switch between INFO and DEBUG logging modes')  # noqa: ignore=E501
def cli(user=None, password=None, verbose=False):
    """Simple program that check a commit message. Try ./get_repo.py -v """

    logger.info('Collecting repo')

    if verbose:
        click.echo(user)
        # click.echo(password)
        click.echo(verbose)

    match_repo(user, password, verbose)


def _get_sha(git_repo, verbose=False):
    """
    Gets the org sha.

    :param git.Remote remote:
    :return: The sha
    :rtype: unicode, unicode
    """
    sha = git_repo.head.object.hexsha
    return sha


def _get_url(git_repo, verbose=False):
    """
    Gets the org url.

    :param git.Remote remote:
    :return: The url
    :rtype: unicode, unicode
    """
    url = git_repo.remotes.origin.url
    return url


def _get_org_and_name_from_remote(url, verbose=False):
    """
    Gets the org name and the repo name from remote.

    :param git.Remote remote:
    :return: The owner and the repo name in that order
    :rtype: unicode, unicode
    """
    if not url.endswith('.git'):
        url = '{}.git'.format(url)
    git_info = parse(url)
    if verbose:
        print('Repo owner: "{}"'.format(git_info.owner))
        print('Repo name: "{}"'.format(git_info.name))
    return git_info.owner, git_info.name


def match_repo(self, user=None, password=None, verbose=False) -> str:

    if verbose:
        logger.setLevel(logging.DEBUG)

    # Figure out which repo we're on
    git_repo = git.Repo(search_parent_directories=True)
    git_root = git_repo.git.rev_parse('--show-toplevel')

    # active_branch = git_repo .active_branch
    # same as name = git_repo .head.ref
    # name = git_repo .head.object.repo.name
    # name = git_repo .head.ref
    url = _get_url(git_repo)
    print(_get_org_and_name_from_remote(url))
    name = os.path.basename(git_root)  # git_repo.working_tree_dir

    print(name)

    # branch = check_output([
    #     'git', 'rev-parse', '--show-toplevel',
    # ]).strip().decode('utf-8')

    return name


logger = logging.getLogger('hooks.get_repo')
logger.setLevel(logging.INFO)
stdoutlog = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutlog)

if __name__ == '__main__':
    cli(None)
