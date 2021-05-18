# -*- coding: utf-8 -*-
import os
import sys
import unittest

# import get_jira.get_auth as script1  # The code to test

# sys.path.append("../hooks")
sys.path.append('./hooks')

# import get_jira.get_jira as script2 # The code to test

# python -m get_jira.get_jira feature/BMT-13403 -v
# python -m get_jira.get_auth -u aandrieu -p XXXX -v
# ./get_msg.py '../.git/COMMIT_EDITMSG'


class TestMyPackage(unittest.TestCase):
    def setUp(self):
        self.local_test_dir = os.path.dirname(os.path.realpath(__file__))

    def test_always_passes(self):
        self.assertTrue


if __name__ == '__main__':
    unittest.main()
