Setup
=====

OS & Python
-----------

Hooks scripts can be run from any modern Linux server or workstation.
We have successfully used Ubuntu 16.04/18.04, CentOS 7.5 and Fedora 29.

Hooks control machine should have ``Python 3.6+`` installed.
On regular basis we are working with versions 3.6 and 3.7.
In case of any problems with running the scripts, upgrading Python should be one of the first things to consider.

Some of the older servers, especially RHEL 5 and x86 Solaris, may still be using Python 2.6 or 2.7 on the remote end.
These exceptions are included in Hooks.
Each of these machines is configured with ``ansible_python_interpreter`` variable.
For most of the new servers or virtual machines, Python 3 is used at the remote as well.
See `Python 3 Support`_ for more details.

Dependencies
------------

Runtime dependencies can be installed using python package manager, ``pip``.
We advise, that you install ansible and other dependencies inside virtual environment.
This will be helpful in case there is problem with any software version.

.. code-block:: bash

   # virtualenv is installed globally on the system
   pip3 install virtualenv==16.1.0

   # all other packages are installed in isolation
   # in general, it is good idea to provide specific python
   # version to the virtualenv (e.g. 3 or 3.6)
   virtualenv -p python3 .venv
   source ./venv/bin/activate
   pip install -r requirements.txt

*Hooks is only true dependency* for this project.
However, certain tasks will require other libraries.
Notably, we are using flake8 and other python librairies for other pre-commit hooks to works.
See PreCommit_ and PreCommitHooks_ for more details.
More on this in the following sections.

Verification
------------

After installing Python modules, following should work::

   $ pre-commit run --all-files

   $ SKIP=ansible-lint git commit -am 'Add key'

   $ git commit -am 'Add key' --no-verify

..  _`Python 3 Support`: http://docs.ansible.com/ansible/latest/python_3_support.html
.. _PreCommit: https://pre-commit.com/
.. _PreCommitHooks: https://github.com/pre-commit/pre-commit-hooks
