## [![Nabla](http://albandrieu.com/nabla/index/assets/nabla/nabla-4.png)](https://github.com/AlbanAndrieu)  nabla-hooks

[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitter](https://badges.gitter.im/nabla-hooks/Lobby.svg)](https://gitter.im/nabla-hooks/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Minimal java version](https://img.shields.io/badge/java-1.8-yellow.svg)](https://img.shields.io/badge/java-1.8-yellow.svg)

[![Jenkins build Status](http://albandrieu.com/jenkins/buildStatus/icon?job=nabla-hooks)](http://albandrieu.com/jenkins/job/nabla-hooks/)
[![Travis Build Status](https://travis-ci.org/AlbanAndrieu/nabla-hooks.svg?branch=master)](https://travis-ci.org/AlbanAndrieu/nabla-hooks)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=MICROSOFT%3Amaster&metric=alert_status)](https://sonarcloud.io/dashboard/index/MICROSOFT%3Amaster)

Nabla custom git hooks

This project intend to be uses by all Nabla products

# Table of contents

<!-- toc -->

- [Requirements](#requirements)
- [Install nabla-hooks as a developer](#install-nabla-hooks-as-a-developer)
  * [Using virtualenv](#using-virtualenv)
- [Install nabla-hooks to use it](#install-nabla-hooks-to-use-it)
  * [Using Pip](#using-pip)
  * [From Source](#from-source)
  * [Add .pre-commit-config.yaml in you git project](#add-pre-commit-configyaml-in-you-git-project)
  * [npm-groovy-lint groovy formating for Jenkinsfile](#npm-groovy-lint-groovy-formating-for-jenkinsfile)
  * [Override global environement variable](#override-global-environement-variable)
  * [Local](#local)
  * [Global](#global)
- [Package nabla-hooks as a developer](#package-nabla-hooks-as-a-developer)
  * [Build a source distribution (a tar archive of all the files needed to build and install the package):](#build-a-source-distribution-a-tar-archive-of-all-the-files-needed-to-build-and-install-the-package)
  * [Upload a source distribution](#upload-a-source-distribution)
- [Test nabla-hooks as a developer](#test-nabla-hooks-as-a-developer)
  * [shell usage](#shell-usage)
  * [Test](#test)
  * [Visual Code](#visual-code)
- [Update README.md](#update-readmemd)

<!-- tocstop -->

## Requirements

  This hooks requires the following to run:

  * [jira](https://pypi.org/project/jira/)

See requirements.txt for mandatory packages.

  This pre-commit hooks requires the following to run:

  * [pre-commit](http://pre-commit.com)

## Install nabla-hooks as a developer

### Using virtualenv

Install python 3.8 and virtualenv

```bash
virtualenv --no-site-packages /opt/ansible/env38 -p python3.8
source /opt/ansible/env38/bin/activate
```

```bash
pip3.8 install -r hooks/requirements.txt -r requirements.testing.txt
```

## Install nabla-hooks to use it

### Using Pip

`pip install nabla-hooks`

### From Source

`pip install git+https://github.com/AlbanAndrieu/nabla-hooks.git`

### Add .pre-commit-config.yaml in you git project

1. create .pre-commit-config.yaml in you git project

example .pre-commit-config.yaml as following:

```yaml
-   repo: https://github.com/AlbanAndrieu/nabla-hooks.git
    rev: v1.0.2
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

2. Install in your repo

Run `pre-commit install`
`pre-commit install -f --install-hooks`

3. enjoy it

Run `pre-commit run --all-files`

Run `SKIP=flake8 git commit -am 'Add key'`
Run `git commit -am 'Add key' --no-verify`


### npm-groovy-lint groovy formating for Jenkinsfile

Tested with nodejs 12 and 16 on ubuntu 20 and 21 (not working with nodejs 11 and 16)

```
npm install -g npm-groovy-lint@8.2.0
npm-groovy-lint --format
ls -lrta .groovylintrc.json
```

### Override global environement variable


#### Login

See [jira](https://jira.readthedocs.io/en/master/examples.html#authentication)

##### With user/pass


```bash
export JIRA_USER=aandrieu
export JIRA_PASSWORD=XXX
export JIRA_URL=https://localhost/jira
export JIRA_CERT_PATH=/etc/ssl/certs/NABLA-CA-1.crt
export JIRA_CERT_PATH=/etc/ssl/certs/ca-certificates.crt
```

##### With email/token

```bash
export JIRA_USER=alban.andrieu@free.fr
export JIRA_PASSWORD=XXX # the token you generated
export JIRA_URL==https://localhost/jira
```

```bash
export JENKINS_URL=https://localhost/jenkins/
export JENKINS_USER=aandrieu
export JENKINS_USER_TOKEN=XXX
```

#### The Templates Directories

See [git-hooks-using-python](http://omerkatz.com/blog/2013/5/23/git-hooks-part-2-implementing-git-hooks-using-python)

### Local

First time run
```bash
cp -r hooks/* .git/hooks/` or `rm -Rf ./.git/hooks/ && ln -s ../hooks ./.git/hooks && git checkout thisrepo hooks/

```

### Global

We have two directories that interest us:

The `/usr/share/git-core/templates/` directory on Linux and `C:/Program Files (x86)/Git/share/git-core/templates/` directory on Windows (Note that on 32bit machines msysGit is installed by default on 'C:/Program Files/…') in which the default hooks are being copied from. If you installed Git using another configuration the installation might reside in a different folder. Adjust the path accordingly.

The `.git/hooks/` directory is the directory in which the hooks templates are being copied to.

The hooked are being copied from the `[...]/share/git-core/templates/` directory.  There are other types of templates but they are out of scope for this post.

Note:  If you change the templates directory the hooks directory  must be a subdirectory of the templates directory. Do not set the templates directory to the desired hooks directory instead.

Run
```bash
git config --global init.templatedir /workspace/users/albandrieu30/nabla-hooks/
```

## Package nabla-hooks as a developer

See [setup-cfg](http://sametmax.com/vive-setup-cfg-et-mort-a-pyproject-toml/)

### Build a source distribution (a tar archive of all the files needed to build and install the package):
`python3 setup.py sdist`
Builds wheels:
`python3 setup.py bdist_wheel`
Build from source:
`python3 setup.py build`
And install:
`/opt/ansible/env38/bin/python3 setup.py install`

`sudo python setup.py develop`
`pip install .`
`pip install -e ./`

### Upload a source distribution

See [api-tokens](https://test.pypi.org/manage/account/#api-tokens)

`
python3 setup.py sdist bdist_wheel
nano $HOME/.pypirc
python3 -m twine upload --repository testpypi dist/*
`

Uploaded [nabla-hooks](https://test.pypi.org/project/nabla-hooks/1.0.2/)

## Test nabla-hooks as a developer

### shell usage

python

`
from hooks import get_msg
match_msg
`

### Test

```bash
tox --notest
tox -e py  # Run tox using the version of Python in PATH
tox py38
```

From root directory

```bash
export PYTHONPATH=hooks
pytest --cache-clear --setup-show test/test_pytest.py
```

### Visual Code

Add PYTHONPATH=hooks for pytest when inside visual studio

```bash
export PYTHONPATH=hooks
echo $PYTHONPATH
code .
```

## Update README.md


  * [github-markdown-toc](https://github.com/jonschlinkert/markdown-toc)
  * With [github-markdown-toc](https://github.com/Lucas-C/pre-commit-hooks-nodejs)

```
npm install --save markdown-toc
markdown-toc README.md
markdown-toc CHANGELOG.md  -i
```

```
pre-commit install
git add README.md
pre-commit run markdown-toc
```
