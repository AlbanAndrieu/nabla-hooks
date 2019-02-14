Setup
=====

OS & Python
-----------

Hooks scripts can be run from any modern Linux server or workstation.
We have successfully used Ubuntu 18.04, CentOS 7.5 and Fedora 29.

Ansible control machine should have ``Python 3.6+`` installed.
On regular basis we are working with versions 3.6 and 3.7.
In case of any problems with running the scripts, upgrading Python should be one of the first things to consider.

Python 2.6 or 2.7 are not more supported.

Dependencies
------------

Runtime dependencies can be installed using python package manager, ``pip``.
We advise, that you install pre-commit and other dependencies inside virtual environment.
This will be helpful in case there is problem with any software version.

.. code-block:: bash

   # virtualenv is installed globally on the system
   pip3 install virtualenv==16.1.0

   # all other packages are installed in isolation
   # in general, it is good idea to provide specific python
   # version to the virtualenv (e.g. 3 or 3.6)
   virtualenv --no-site-packages /opt/ansible/env36 -p python3.6
   source /opt/ansible/env36/bin/activate
   pip install -r requirements-current-3.6.txt

Initialization
------------

.. code-block:: bash

   export JIRA_USER=aandrieu
   export JIRA_PASSWORD=XXX


Verification
------------

After installing Python modules, following should work::

   $ python -m get_jira.test.check_certificates

   $ hooks/test.sh

..  _`Python 3 Support`: http://docs.ansible.com/ansible/latest/python_3_support.html
