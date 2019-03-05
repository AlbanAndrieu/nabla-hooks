Roles
=================

These commits hooks allow you to validate your commit message against JIRA.

Then run the hook, do like this::

	git commit -am 'Add your commit message without the JIRA'

When the hooks run completes, you should be able to have the JIRA automatically retreive from the branch name and validated against JIRA.

This is a very simple hook and could serve as a starting point for more complex hooks.

Use cases
---------

 - The JIRA number will be retreived from the feature or bugfix branches and check against JIRA.
 - This JIRA will be added in the commit message if not found. This feature is needed, because whithout squashing feature git changelog (in Jenkins) will be unable to find the JIRA ans display proper information
 - The JIRA status to be a valid JIRA should not be `Closed` or `Done`

Improvments && TODO
-------------------

So far JIRA status is checked among `Closed` or `Done`. But for issue type Story, for BugFix or Backport status might be different

Minimal Python
~~~~~~~~~~~~~~~~~~~~~

See requirements.txt for python 3.6
