# nabla-hooks

[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitter](https://badges.gitter.im/nabla-hooks/Lobby.svg)](https://gitter.im/nabla-hooks/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Minimal java version](https://img.shields.io/badge/java-1.8-yellow.svg)](https://img.shields.io/badge/java-1.8-yellow.svg)

[![Jenkins build Status](http://albandrieu.com:8686/job/nabla-hooks/badge/icon)](http://albandrieu.com:8686/job/nabla-hooks/)
[![Travis Build Status](https://travis-ci.org/AlbanAndrieu/nabla-hooks.svg?branch=master)](https://travis-ci.org/AlbanAndrieu/nabla-hooks)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=MICROSOFT%3Amaster&metric=alert_status)](https://sonarcloud.io/dashboard/index/MICROSOFT%3Amaster)

Nabla custom git hooks

This project intend to be uses by all Nabla products

Table of Contents
-----------------

  * [Requirements](#requirements)
  * [Install](#install)
  * [Quality tools](#qualitytools)

Requirements
------------
  This pre-commit hooks requires the following to run:

  * [pre-commit](http://pre-commit.com)


Install pre-commit
------------------

1. create .pre-commit-config.yaml in you git project
2. pre-commit install
3. enjoy it

example .pre-commit-config.yaml as following:

```yaml
-   repo: https://github.com/AlbanAndrieu/nabla-hooks.git
    rev: v1.0.0
    hooks:
    - id: git-branches-check
```

Testing locally

```yaml
-   repo: local
    hooks:
    -   id: git-branches-check
        name: GIT branches check
        description: Check for old stale and already merged branches from the current repo with user friendly messages and colors
        entry: pre_commit_hooks/git-branches-check.sh
        language: script
        types: [shell]
        always_run: true
        verbose: true
        args: [--max=1, --verbose]
```

$ `pre-commit try-repo . git-branches-check --verbose`

Install custom hooks
------------------

### Using Pip

`pip install hook`

### From Source

`pip install git+https://github.com/AlbanAndrieu/nabla-hooks.git`

Quality tools
-------------

### python 3.7

Install python 3.7 and virtualenv

`virtualenv --no-site-packages /opt/ansible/env37 -p python3.7`

`source /opt/ansible/env37/bin/activate`

`pip install -r requirements-current-3.7.txt`

### pre-commit

See [pre-commit](http://pre-commit.com/)

Run `pre-commit install`
`pre-commit install -f --install-hooks`

Run `pre-commit run --all-files`

Run `SKIP=flake8 git commit -am 'Add key'`
Run `git commit -am 'Add key' --no-verify`

### pre-commit specific hook

`export JIRA_USER=aandrieu`

`export JIRA_PASSWORD=XXX`

`export JIRA_URL=https://localhost/jira`

`export JIRA_CERT_PATH=/etc/ssl/certs/NABLA-CA-1.crt`

`export JENKINS_URL=https://localhost/jenkins/`

`export JENKINS_USER=aandrieu`

`export JENKINS_USER_TOKEN=117e17192512cebff9e0009d752f9e2b29`

### The Templates Directories

See [git-hooks-using-python](http://omerkatz.com/blog/2013/5/23/git-hooks-part-2-implementing-git-hooks-using-python)

## Local

First time run `cp hooks/* .git/hooks/` or `rm -Rf ./.git/hooks/ && ln -s ../hooks ./.git/hooks && git checkout thisrepo hooks/`

## Global

We have two directories that interest us:

The '/usr/share/git-core/templates/' directory on Linux and 'C:/Program Files (x86)/Git/share/git-core/templates/' directory on Windows (Note that on 32bit machines msysGit is installed by default on 'C:/Program Files/…') in which the default hooks are being copied from. If you installed Git using another configuration the installation might reside in a different folder. Adjust the path accordingly.
The '.git/hooks/' directory is the directory in which the hooks templates are being copied to.
The hooked are being copied from the '[...]/share/git-core/templates/'  directory.  There are other types of templates but they are out of scope for this post.

Note:  If you change the templates directory the hooks directory  must be a subdirectory of the templates directory. Do not set the templates directory to the desired hooks directory instead.

Run `git config --global init.templatedir /workspace/users/albandrieu30/nabla-hooks/`

### packaging

See [setup-cfg](http://sametmax.com/vive-setup-cfg-et-mort-a-pyproject-toml/)

# Builds a source distribution (a tar archive of all the files needed to build and install the package):
`python setup.py sdist`
Builds wheels:
`python setup.py bdist_wheel`
Build from source:
`python setup.py build`
And install:
`python setup.py install`

`sudo python setup.py develop`
`pip install .`
`pip install -e ./`

# [api-tokens](https://test.pypi.org/manage/account/#api-tokens)

`
python3 setup.py sdist bdist_wheel
nano $HOME/.pypirc
python3 -m twine upload --repository testpypi dist/*
`

Uploaded [nabla-hooks](https://test.pypi.org/project/nabla-hooks/0.0.1/)

### shell usage

python

`
from hooks import get_msg
match_msg
`
