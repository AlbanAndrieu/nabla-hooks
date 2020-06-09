#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import re
import sys
import traceback
from subprocess import check_output  # nosec

import click
import get_jira.get_auth
import get_jira.get_jira
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

__all__ = ['match_msg']


@click.command()
@click.argument('commit_msg_filepath', type=click.Path(exists=False))
@click.argument('commit_type', type=str, default='')  # message for prepare-commit-msg
@click.option('-u', '--user', required=False, envvar='JIRA_USER', help='JIRA user')  # noqa: ignore=E501
@click.option('-p', '--password', required=False, prompt=True, hide_input=True, confirmation_prompt=True, envvar='JIRA_PASSWORD', help='JIRA password')  # noqa: ignore=E501
@click.option('-v', '--verbose', is_flag=True, default=False, help='Switch between INFO and DEBUG logging modes')  # noqa: ignore=E501
def cli(commit_msg_filepath, commit_type: str = '', user=None, password=None, verbose=False):
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

    logger.info('Collecting branch')

    if verbose:
        click.echo(click.format_filename(commit_msg_filepath))
        click.echo(user)
        # click.echo(password)
        click.echo(verbose)

    return match_msg(
        commit_msg_filepath=commit_msg_filepath, commit_type=commit_type,
        user=user, password=password, verbose=verbose,
    )


def match_msg(commit_msg_filepath: str, commit_type: str = '', user=None, password=None, verbose=False) -> str:
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
        basic_auth = get_jira.get_auth.match_auth(
            user=user, password=password, verbose=verbose,
        )

        # Figure out which branch we're on
        branch = check_output([
            '/usr/bin/git', 'symbolic-ref', '--short',
            'HEAD',
        ]).strip().decode('utf-8')

        logger.debug(r"msg: On branch '{}'".format(branch))
        regex = re.compile('^feature|^bugfix')

        filename = os.path.expanduser(commit_msg_filepath)
        required_message = ''

        if os.path.exists(filename):
            with open(commit_msg_filepath, 'r+') as f:
                current_message = f.read()
                f.seek(0, 0)

            if not current_message:
                print(
                    colored(
                        'Current message is empty.', 'red',
                    ),
                )
            else:
                if verbose:
                    print(
                        colored(
                            'Message before is : {}'.format(
                                current_message,
                            ), 'yellow',
                        ),
                    )

            # Populate the commit message with the issue #, if there is one
            if re.match(regex, branch):
                if 'message' in commit_type:
                    print(
                        colored(
                            "Oh hey, it's an issue branch : {}.".format(
                                branch,
                            ), 'green',
                        ),
                    )

                msg = get_jira.get_jira.get_msg(
                    current_message=current_message, branch=branch, basic_auth=basic_auth, verbose=verbose,
                )

                required_message = msg[0]

                if not required_message:
                    # Required message is empty
                    required_message = current_message

                if verbose:
                    print(
                        colored(
                            'Message after is : {}'.format(
                                required_message,
                            ), 'yellow',
                        ),
                    )
                with open(commit_msg_filepath, 'r+') as f:
                    f.seek(0, 0)
                    f.write('{}'.format(required_message))

        return required_message

    except:  # noqa: ignore=E722
        traceback.print_exc()
        sys.exit(2)


logger = logging.getLogger('hooks.get_msg')
logger.setLevel(logging.INFO)
stdoutlog = logging.StreamHandler(sys.stdout)
logger.addHandler(stdoutlog)

if __name__ == '__main__':
    cli(None)
