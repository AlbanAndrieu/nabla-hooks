Library
=======

Library consists of custom Hooks modules, that can be used with any role or playbook in this repository.

Using modules more systematic way of doing certain tasks.
For example, we provide ``get_jira`` module, which allows to acces to JIRA.
This task could be done using Hooks's built-in ``python`` module and ``pre-commit`` command line tool.

In this case, module is advantageous, because it provides more control over catching exceptions or determining the "failed" and "changed" results.

I am using open source librairies such as Jira_ or Git-url-parse_ and _GitPython
Library files are placed in is in ``./hooks/get_jira/``. See below for the module documentation.

.. automodule:: hooks/get_jira
   :members: main

.. automodule:: get_msg
   :members: main

.. automodule:: get_repo
   :members: main

.. _Jira: https://jira.readthedocs.io/en/master/
.. _Git-url-parse: https://pypi.org/project/git-url-parse/
.. _GitPython: https://github.com/gitpython-developers/GitPython
