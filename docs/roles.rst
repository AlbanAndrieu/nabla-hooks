Roles & Playbooks
=================

TODO - it should be the most exhaustive section.

These commits hooks allow you to validate your commit message against JIRA.

Then run the hook, do like this::

	git commit -am 'Add your commit message without the JIRA'

When the hooks run completes, you should be able to have the JIRA automatically retreive from the branch name and validated agains JIRA.

This is a very simple hook and could serve as a starting point for more complex hooks.

Use cases
---------

Minimal Python
~~~~~~~~~~~~~~~~~~~~~

See requirements.txt for python 3.6
