#!/bin/bash
#set -eu

python -m get_jira.get_jira feature/BMT-13403 -v
python -m get_jira.get_auth -u aandrieu -p XXXX -v
./get_msg.py '../.git/COMMIT_EDITMSG'

exit 0
