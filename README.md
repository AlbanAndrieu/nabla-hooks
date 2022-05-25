<!-- markdown-link-check-disable-next-line -->
## [![Nabla](http://albandrieu.com/nabla/index/assets/nabla/nabla-4.png)](https://github.com/AlbanAndrieu)  nabla-hooks

Nabla custom git hooks

[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitter](https://badges.gitter.im/nabla-hooks/Lobby.svg)](https://gitter.im/nabla-hooks/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

[![Jenkins build Status](http://albandrieu.com/jenkins/buildStatus/icon?job=nabla-hooks)](http://albandrieu.com/jenkins/job/nabla-hooks/)
[![Travis Build Status](https://travis-ci.org/AlbanAndrieu/nabla-hooks.svg?branch=master)](https://travis-ci.org/AlbanAndrieu/nabla-hooks)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nabla%3Anabla-hooks&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nabla%3Anabla-hooks)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/AlbanAndrieu/nabla-hooks.svg)](https://github.com/AlbanAndrieu/nabla-hooks/pulls)

This project intend to be uses by all Nabla products

# Table of contents

<!-- markdown-link-check-disable -->

// spell-checker:disable

<!-- toc -->

- [Requirements](#requirements)
- [Install nabla-hooks as a developer](#install-nabla-hooks-as-a-developer)
  * [Using virtualenv](#using-virtualenv)
- [Install nabla-hooks to use it](#install-nabla-hooks-to-use-it)
  * [Using Pip](#using-pip)
  * [From Source](#from-source)
  * [Add .pre-commit-config.yaml in you git project](#add-pre-commit-configyaml-in-you-git-project)
  * [Override global environment variable](#override-global-environment-variable)
  * [Local](#local)
  * [Global](#global)
- [Package nabla-hooks as a developer](#package-nabla-hooks-as-a-developer)
  * [Build a source distribution (a tar archive of all the files needed to build and install the package):](#build-a-source-distribution-a-tar-archive-of-all-the-files-needed-to-build-and-install-the-package)
  * [Upload a source distribution](#upload-a-source-distribution)
- [Test nabla-hooks as a developer](#test-nabla-hooks-as-a-developer)
  * [shell usage](#shell-usage)
  * [versioneer](#versioneer)
  * [Test](#test)
  * [Poetry](#poetry)
  * [Pdm](#pdm)
- [Update README.md](#update-readmemd)
- [npm-groovy-lint groovy formatting for Jenkinsfile](#npm-groovy-lint-groovy-formatting-for-jenkinsfile)

<!-- tocstop -->

// spell-checker:enable

<!-- markdown-link-check-enable -->

## Requirements

  This hooks requires the following to run:

<!-- markdown-link-check-disable-next-line -->
  * [jira](https://pypi.org/project/jira/)

See requirements.txt for mandatory packages.

  This pre-commit hooks requires the following to run:

<!-- markdown-link-check-disable-next-line -->
  * [pre-commit](http://pre-commit.com)

## Install nabla-hooks as a developer

### Using virtualenv

Install python 3.8 and virtualenv

```bash
virtualenv --no-site-packages /opt/ansible/env38 -p python3.8
source /opt/ansible/env38/bin/activate
```

Install python 3.8 and pyenv

```bash
curl -L https://pyenv.run | bash
echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv install 3.8.6
```

and [integrate](https://stackabuse.com/managing-python-environments-with-direnv-and-pyenv/) it with direnv

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
    rev: v1.0.3
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


### Override global environment variable


#### Login

See [jira](https://jira.readthedocs.io/en/master/examples.html#authentication)

##### With user/pass


<!-- markdown-link-check-disable -->
```bash
export JIRA_USER=aandrieu
export JIRA_PASSWORD=XXX
export JIRA_URL=https://localhost/jira
export JIRA_CERT_PATH=/etc/ssl/certs/NABLA-CA-1.crt
export JIRA_CERT_PATH=/etc/ssl/certs/ca-certificates.crt
```
<!-- markdown-link-check-enable -->

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
cp -r hooks/* .git/hooks/` or `rm -Rf ./.git/hooks/ && ln -s ../hooks ./.git/hooks && git checkout repo hooks/

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

```bash
rm -Rf dist/
python3 setup.py sdist bdist_wheel
# Check package
twine check dist/*
nano $HOME/.pypirc
export TWINE_PASSWORD=pypi-
python3 -m twine upload --repository nabla-hooks dist/* --verbose
```

All in one

```bash
python setup.py register sdist upload
```

Uploaded [nabla-hooks](https://test.pypi.org/project/nabla-hooks/)

## Test nabla-hooks as a developer

### shell usage

python

```python
from hooks import get_msg
match_msg
```

### versioneer

[versioneer](https://github.com/python-versioneer/python-versioneer)

```bash
versioneer install
#check with
python setup.py version
python setup.py install
```

### Test

```bash
tox --notest
tox -e py  # Run tox using the version of Python in PATH
tox py38
```

From root directory

```bash
pytest --cache-clear --setup-show hooks/test/test_pytest.py
pytest --cache-clear --setup-show test/package.py
```

### Poetry

```bash
poetry install
poetry env info
poetry shell
poetry run pytest
poetry build
#poetry publish --build
```

### Pdm

[pdm](https://pdm.fming.dev/)

```bash
pdm init
pdm run flake8
```

## Update README.md


  * [github-markdown-toc](https://github.com/jonschlinkert/markdown-toc)
  * With [github-markdown-toc](https://github.com/Lucas-C/pre-commit-hooks-nodejs)

```bash
npm install --save markdown-toc
markdown-toc README.md -i
markdown-toc CHANGELOG.md -i
```

```bash
pre-commit install
git add README.md
pre-commit run markdown-toc
```

Check syntax
[remark-lint](https://github.com/remarkjs/remark-lint#cli)


```bash
npm run lint-md
```

## npm-groovy-lint groovy formatting for Jenkinsfile

Tested with nodejs 12 and 16 on ubuntu 20 and 21 (not working with nodejs 11 and 16)

```bash
npm install -g npm-groovy-lint@8.2.0
npm-groovy-lint --format
ll .groovylintrc.json
```
