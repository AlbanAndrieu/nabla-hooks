<!-- markdown-link-check-disable-next-line -->

# [![Nabla](https://nabla.albandrieu.com/assets/nabla/nabla-4.png)](https://github.com/AlbanAndrieu) nabla-hooks

Nabla custom git hooks

[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitter](https://badges.gitter.im/nabla-hooks/Lobby.svg)](https://gitter.im/nabla-hooks/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Python package](https://github.com/AlbanAndrieu/nabla-hooks/actions/workflows/python.yml/badge.svg)](https://github.com/AlbanAndrieu/nabla-hooks/actions/workflows/python.yml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nabla%3Anabla-hooks&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nabla%3Anabla-hooks)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/AlbanAndrieu/nabla-hooks.svg)](https://github.com/AlbanAndrieu/nabla-hooks/pulls)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAlbanAndrieu%2Fnabla-hooks.svg?type=shield&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FAlbanAndrieu%2Fnabla-hooks?ref=badge_shield&issueType=license)

This project intend to be uses by all Nabla products

This project is DEPRECATED, commit validation will now be done using [commitizen](https://commitizen-tools.github.io/commitizen/customization/) or [commitlint](https://commitlint.js.org/) still using pre-commit or [opencommit](https://github.com/di-sukharev/opencommit)

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](.github/CONTRIBUTING.md) for details on:

- Setting up your development environment with Poetry
- Running tests and code quality checks
- Submitting pull requests
- GitHub workflows and CI/CD

For issues, feature requests, or questions, please use our [GitHub issue templates](.github/ISSUE_TEMPLATE/).

# Table of contents

<!-- markdown-link-check-disable -->

// spell-checker:disable

<!-- toc -->

- [Initialize](#initialize)
  * [Requirements](#requirements)
  * [Install nabla-hooks as a developer](#install-nabla-hooks-as-a-developer)
    + [Using virtualenv](#using-virtualenv)
  * [Install nabla-hooks to use it](#install-nabla-hooks-to-use-it)
    + [Using Pip](#using-pip)
    + [From Source](#from-source)
    + [Add .pre-commit-config.yaml in you git project](#add-pre-commit-configyaml-in-you-git-project)
    + [Override global environment variable](#override-global-environment-variable)
    + [Local](#local)
    + [Global](#global)
  * [Package nabla-hooks as a developer](#package-nabla-hooks-as-a-developer)
    + [Build a source distribution (a tar archive of all the files needed to build and install the package):](#build-a-source-distribution-a-tar-archive-of-all-the-files-needed-to-build-and-install-the-package)
    + [Upload a source distribution](#upload-a-source-distribution)
  * [Test nabla-hooks as a developer](#test-nabla-hooks-as-a-developer)
    + [shell usage](#shell-usage)
    + [versioneer](#versioneer)
    + [Test](#test)
    + [Poetry](#poetry)
    + [Pdm](#pdm)
  * [Update README.md](#update-readmemd)
  * [npm-groovy-lint groovy formatting for Jenkinsfile](#npm-groovy-lint-groovy-formatting-for-jenkinsfile)

<!-- tocstop -->

// spell-checker:enable

<!-- markdown-link-check-enable -->

# [Initialize](#table-of-contents)

## Quick Start with Poetry (Recommended)

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
# Install pyenv and Python (recommended)
pyenv install 3.12.10
pyenv local 3.12.10

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests to verify setup
poetry run pytest
```

## Alternative: Using pipenv (Legacy)

```bash
direnv allow
pyenv install 3.10.9
pyenv local 3.10.9
python -m pipenv install --dev --ignore-pipfile
direnv allow
pre-commit install
```

## Migration from Pipenv to Poetry

If you're migrating from Pipenv:

```bash
pip install -U poetry pipenv-poetry-migrate
pipenv-poetry-migrate -f Pipfile -t pyproject.toml --no-use-group-notation
```

## [Requirements](#table-of-contents)

This hooks requires the following to run:

<!-- markdown-link-check-disable-next-line -->

- [jira](https://pypi.org/project/jira/)

See requirements.txt for mandatory packages.

This pre-commit hooks requires the following to run:

<!-- markdown-link-check-disable-next-line -->

- [pre-commit](http://pre-commit.com)

## [Install nabla-hooks as a developer](#table-of-contents)

### Using virtualenv

Install python 3.10 and virtualenv

```bash
virtualenv --no-site-packages /opt/ansible/env312 -p python3.12
source /opt/ansible/env312/bin/activate
```

Install python 3.8 and pyenv

```bash
curl -L https://pyenv.run | bash
echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv install 3.12.10
```

and [integrate](https://stackabuse.com/managing-python-environments-with-direnv-and-pyenv/) it with direnv

```bash
#pip3 install -r hooks/requirements.txt -r requirements.testing.txt
pipenv check
python -m pipenv install --dev
python -m pipenv install --dev --ignore-pipfile
```

## [Install nabla-hooks to use it](#table-of-contents)

### Using Pip

`pip install nabla-hooks`

### From Source

`pip install git+https://github.com/AlbanAndrieu/nabla-hooks.git`

### Add .pre-commit-config.yaml in you git project

1. create .pre-commit-config.yaml in you git project

example .pre-commit-config.yaml as following:

```yaml
-   repo: https://github.com/AlbanAndrieu/nabla-hooks.git
    rev: v1.0.7
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

[auto_prepare_commit_message](https://commitizen-tools.github.io/commitizen/tutorials/auto_prepare_commit_message/)

```bash
wget -O .git/hooks/prepare-commit-msg https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/prepare-commit-msg.py
chmod +x .git/hooks/prepare-commit-msg
wget -O .git/hooks/post-commit https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/post-commit.py
chmod +x .git/hooks/post-commit
```

### Global

We have two directories that interest us:

The `/usr/share/git-core/templates/` directory on Linux and `C:/Program Files (x86)/Git/share/git-core/templates/` directory on Windows (Note that on 32bit machines msysGit is installed by default on 'C:/Program Files/…') in which the default hooks are being copied from. If you installed Git using another configuration the installation might reside in a different folder. Adjust the path accordingly.

The `.git/hooks/` directory is the directory in which the hooks templates are being copied to.

The hooked are being copied from the `[...]/share/git-core/templates/` directory. There are other types of templates but they are out of scope for this post.

Note: If you change the templates directory the hooks directory must be a subdirectory of the templates directory. Do not set the templates directory to the desired hooks directory instead.

Run

```bash
git config --global --get init.templatedir
rm -Rf .git/hooks
git config --global init.templatedir /workspace/users/albandrieu30/nabla-hooks/
```

## Package nabla-hooks as a developer

See [setup-cfg](http://sametmax.com/vive-setup-cfg-et-mort-a-pyproject-toml/)

### Build a source distribution (a tar archive of all the files needed to build and install the package):

`python -m build`

`pip install .`
`pip install -e ./`

### Upload a source distribution

See [api-tokens](https://test.pypi.org/manage/account/#api-tokens)

```bash
rm -Rf dist/
pip install setuptools
python3 setup.py sdist bdist_wheel
# Check package
twine check dist/*
nano $HOME/.pypirc
export TWINE_PASSWORD=pypi-
python3 -m twine upload --repository nabla-hooks dist/* --verbose
```

See [nabla-hooks-1.0.7](https://pypi.org/project/nabla-hooks/1.0.7/)

Uploaded [nabla-hooks](https://test.pypi.org/project/nabla-hooks/)

## [Test nabla-hooks as a developer](#table-of-contents)

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
source deactivate
tox --notest
tox -e py  # Run tox using the version of Python in PATH
tox -e py312
```

From root directory

```bash
pytest --cache-clear --setup-show hooks/tests/pytest_test.py
pytest --cache-clear --setup-show tests/test_package.py
```

### Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

#### Quick Start with Poetry

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate the virtual environment
poetry shell

# Run tests
poetry run pytest

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

#### Poetry Commands

```bash
# Show environment information
poetry env info

# Show installed packages
poetry show

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Build the package
poetry build

# Publish to PyPI (requires authentication)
# https://python-poetry.org/docs/repositories/
poetry config pypi-token.pypi ${TWINE_PASSWORD}
poetry publish --build

# Check pyproject.toml for errors
poetry check

# Lock dependencies without installing
poetry lock
```

For more details, see the [CONTRIBUTING.md](.github/CONTRIBUTING.md) guide.

### Pdm

[pdm](https://pdm.fming.dev/)

```bash
pdm init
pdm run flake8
```

## [GitHub Workflows and CI/CD](#table-of-contents)

This project uses GitHub Actions for continuous integration and deployment. The following workflows are configured:

### Available Workflows

1. **Python Package** (`.github/workflows/python.yml`)
   - Runs on: Push to master, Pull requests
   - Tests on: Python 3.12 and 3.13
   - Steps: Lint (flake8, pylint, bandit), Test (pytest, tox)
   - Badge: ![Python package](https://github.com/AlbanAndrieu/nabla-hooks/actions/workflows/python.yml/badge.svg)

2. **CodeQL Analysis** (`.github/workflows/codeql.yml`)
   - Security scanning for code vulnerabilities
   - Runs on: Push and Pull requests

3. **Linter** (`.github/workflows/linter.yml`)
   - Comprehensive linting across the project
   - Uses MegaLinter for multiple file types

4. **Release** (`.github/workflows/release.yml`)
   - Automated release creation and publishing

5. **Tests** (`.github/workflows/tests.yml`)
   - Dedicated test workflow

### Workflow Requirements

All pull requests must pass:
- ✅ Linting (flake8, pylint, bandit)
- ✅ Tests (pytest with >30% coverage)
- ✅ Code quality checks (SonarCloud)
- ✅ Security scanning (CodeQL)

### Local CI Simulation

Before pushing, run the same checks locally:

```bash
# Activate poetry environment
poetry shell

# Run linters
poetry run flake8 hooks tests
poetry run pylint hooks
poetry run bandit -r hooks

# Run tests
poetry run pytest --cov=hooks --cov-fail-under=30

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

For more details, see [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## [Update README.md](#table-of-contents)

- [github-markdown-toc](https://github.com/jonschlinkert/markdown-toc)
- With [github-markdown-toc](https://github.com/Lucas-C/pre-commit-hooks-nodejs)

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

## [npm-groovy-lint groovy formatting for Jenkinsfile](#table-of-contents)

Tested with nodejs 12 and 16 on ubuntu 20 and 21 (not working with nodejs 11 and 16)

```bash
npm install -g npm-groovy-lint@8.2.0
npm-groovy-lint --format
ll .groovylintrc.json
```
