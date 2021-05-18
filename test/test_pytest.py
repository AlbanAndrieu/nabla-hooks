# -*- coding: utf-8 -*-
import re
import sys

import get_jira.get_auth as script1  # The code to test
import get_jira.get_jira as script2  # The code to test
import pytest
# from hooks import get_msg # NOK

# sys.path.append("../hooks")
sys.path.append('./hooks')


# python -m get_jira.get_jira feature/BMT-13403 -v
# python -m get_jira.get_auth -u aandrieu -p XXXX -v
# ./get_msg.py '../.git/COMMIT_EDITMSG'


def test_always_passes():
    assert True

# def test_always_fails():
#    assert False


def test_get_user():
    assert script1.get_user('') == 'aandrieu'


def test_get_user_nok():
    assert script1.get_user('') != 'toto'


def test_get_jira_url():
    my_url = script2.get_jira_url()
    print(my_url)
    # url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", re.IGNORECASE)
    url_regex = re.compile(r'^\w+')
    r1 = re.findall(url_regex, 'https://localhost/jira')
    print(r1)
    z = url_regex.match(my_url)
    if z:
        print(z.groups)
    assert url_regex.match(my_url)
    # Matches.from_pattern(url_regex) == 'https://localhost/jira'
    # assert script2.get_jira_url() == "https://localhost/jira"


def myfunc():
    raise ValueError('https://localhost/jira')


def test_match():
    with pytest.raises(ValueError) as excinfo:
        myfunc()
    excinfo.match(r'.*localhost.*')


def test_get_certificat_path():
    assert script2.get_certificat_path() == '/etc/ssl/certs/ca-certificates.crt'

# @pytest.mark.timeout(10)
# def test_get_msg():
#    assert script2.get_msg("test", "feature/BMT-13403") == "toto"
