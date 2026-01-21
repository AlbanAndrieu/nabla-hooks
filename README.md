<!-- markdown-link-check-disable-next-line -->

# [![Nabla](https://nabla.albandrieu.com/assets/nabla/nabla-4.png)](https://github.com/AlbanAndrieu) nabla-hooks

Nabla custom git hooks

[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitter](https://badges.gitter.im/nabla-hooks/Lobby.svg)](https://gitter.im/nabla-hooks/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=nabla%3Anabla-hooks&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=nabla%3Anabla-hooks)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/AlbanAndrieu/nabla-hooks.svg)](https://github.com/AlbanAndrieu/nabla-hooks/pulls)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FAlbanAndrieu%2Fnabla-hooks.svg?type=shield&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2FAlbanAndrieu%2Fnabla-hooks?ref=badge_shield&issueType=license)

This project provides custom Git hooks for code quality validation and is intended to be used by all Nabla products.

**Note:** This project is in maintenance mode. For new projects, we recommend using [commitizen](https://commitizen-tools.github.io/commitizen/customization/), [commitlint](https://commitlint.js.org/), or [opencommit](https://github.com/di-sukharev/opencommit) with pre-commit hooks.

## Features

- **Git Branches Check**: Validates old stale and already merged branches
- **Jenkinsfile Validation**: Checks Jenkinsfile syntax and formatting
- **JIRA Integration**: Optional JIRA ticket validation in commit messages
- **Pre-commit Hooks**: Integrates with the pre-commit framework

## Quick Start

### Installation

Install using pip:

```bash
pip install nabla-hooks
```

Or from source:

```bash
pip install git+https://github.com/AlbanAndrieu/nabla-hooks.git
```

### Usage

1. Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/AlbanAndrieu/nabla-hooks.git
    rev: v1.0.7
    hooks:
      - id: git-branches-check
```

2. Install pre-commit hooks:

```bash
pre-commit install
```

3. Run on all files:

```bash
pre-commit run --all-files
```

# Table of contents

<!-- markdown-link-check-disable -->

// spell-checker:disable

<!-- toc -->

- [Features](#features)
- [Quick Start](#quick-start)
  * [Installation](#installation)
  * [Usage](#usage)
- [Initialize](#initialize)
  * [Requirements](#requirements)
  * [Install nabla-hooks as a developer](#install-nabla-hooks-as-a-developer)
    + [Using virtualenv](#using-virtualenv)
  * [Install nabla-hooks to use it](#install-nabla-hooks-to-use-it)
    + [Using Pip](#using-pip)
    + [From Source](#from-source)
    + [Add .pre-commit-config.yaml in your git project](#add-pre-commit-configyaml-in-your-git-project)
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

## Development Setup

Using pipenv with Pipfile:

```bash
direnv allow
pyenv install 3.12.10
pyenv local 3.12.10
python -m pipenv install --dev --ignore-pipfile
direnv allow
pre-commit install
```

Using poetry with pyproject.toml:

```bash
pip install -U poetry pipenv-poetry-migrate
pipenv-poetry-migrate -f Pipfile -t pyproject.toml --no-use-group-notation
```

## [Requirements](#table-of-contents)

### Runtime Requirements

This package requires the following to run:

- Python >= 3.9
- [pre-commit](http://pre-commit.com)
- [jira](https://pypi.org/project/jira/) (optional, for JIRA integration)

See `requirements.txt` for the complete list of Python dependencies.

## [Install nabla-hooks as a developer](#table-of-contents)

### Using virtualenv

Install Python 3.12 and virtualenv:

```bash
virtualenv --no-site-packages /opt/ansible/env312 -p python3.12
source /opt/ansible/env312/bin/activate
```

Install Python 3.12 with pyenv:

```bash
curl -L https://pyenv.run | bash
echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source ~/.bashrc

pyenv install 3.12.10
```

See [pyenv with direnv integration](https://stackabuse.com/managing-python-environments-with-direnv-and-pyenv/) for more details.

```bash
pipenv check
python -m pipenv install --dev
python -m pipenv install --dev --ignore-pipfile
```

## [Install nabla-hooks to use it](#table-of-contents)

### Using Pip

`pip install nabla-hooks`

### From Source

`pip install git+https://github.com/AlbanAndrieu/nabla-hooks.git`

### Add .pre-commit-config.yaml in your git project

1. Create `.pre-commit-config.yaml` in your git project

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/AlbanAndrieu/nabla-hooks.git
    rev: v1.0.7
    hooks:
      - id: git-branches-check
```

For local testing:

```yaml
repos:
  - repo: local
    hooks:
      - id: git-branches-check
        name: GIT branches check
        description: Check for old stale and already merged branches from the current repo with user friendly messages and colors
        entry: pre_commit_hooks/git-branches-check.sh
        language: script
        types: [shell]
        always_run: true
        verbose: true
        args: [--max=1, --verbose]
```

Test locally:

```bash
pre-commit try-repo . git-branches-check --verbose
```

2. Install pre-commit hooks in your repository

```bash
pre-commit install
# Or force reinstall
pre-commit install -f --install-hooks
```

3. Run pre-commit on all files

```bash
pre-commit run --all-files
```

To skip specific hooks:

```bash
SKIP=flake8 git commit -am 'Add key'
# Or bypass all hooks
git commit -am 'Add key' --no-verify
```

### Override global environment variable

#### Authentication

See [JIRA authentication documentation](https://jira.readthedocs.io/en/master/examples.html#authentication)

##### Using username/password

```bash
export JIRA_USER=aandrieu
export JIRA_PASSWORD=XXX
export JIRA_URL=https://localhost/jira
export JIRA_CERT_PATH=/etc/ssl/certs/NABLA-CA-1.crt
# Or use system CA bundle
export JIRA_CERT_PATH=/etc/ssl/certs/ca-certificates.crt
```

##### Using email/token

```bash
export JIRA_USER=alban.andrieu@free.fr
export JIRA_PASSWORD=XXX  # Your generated API token
export JIRA_URL=https://localhost/jira
```

##### Jenkins authentication

```bash
export JENKINS_URL=https://localhost/jenkins/
export JENKINS_USER=aandrieu
export JENKINS_USER_TOKEN=XXX
```

#### Git Hooks Templates

See [implementing git hooks using Python](http://omerkatz.com/blog/2013/5/23/git-hooks-part-2-implementing-git-hooks-using-python)

### Local

First time setup:

```bash
# Copy hooks to .git/hooks
cp -r hooks/* .git/hooks/
# Or create symbolic link
rm -Rf ./.git/hooks/ && ln -s ../hooks ./.git/hooks && git checkout repo hooks/
```

Using [auto_prepare_commit_message](https://commitizen-tools.github.io/commitizen/tutorials/auto_prepare_commit_message/):

```bash
wget -O .git/hooks/prepare-commit-msg https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/prepare-commit-msg.py
chmod +x .git/hooks/prepare-commit-msg
wget -O .git/hooks/post-commit https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/post-commit.py
chmod +x .git/hooks/post-commit
```

### Global

Git uses template directories to initialize new repositories. We have two relevant directories:

- **Linux**: `/usr/share/git-core/templates/`
- **Windows**: `C:/Program Files (x86)/Git/share/git-core/templates/` (or `C:/Program Files/...` on 32-bit)

The hooks are copied from `[...]/share/git-core/templates/` directory to `.git/hooks/` when initializing a new repository.

**Note:** If you change the templates directory, the hooks directory must be a subdirectory of the templates directory. Do not set the templates directory to the desired hooks directory.

Setup:

```bash
git config --global --get init.templatedir
rm -Rf .git/hooks
git config --global init.templatedir /workspace/users/albandrieu30/nabla-hooks/
```

## Package nabla-hooks as a developer

See [setup.cfg documentation](http://sametmax.com/vive-setup-cfg-et-mort-a-pyproject-toml/)

### Build a source distribution (a tar archive of all the files needed to build and install the package):

```bash
python -m build
```

Install locally:

```bash
pip install .
# Or in editable mode
pip install -e ./
```

### Upload a source distribution

See [PyPI API tokens](https://test.pypi.org/manage/account/#api-tokens)

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

Published versions:
- Production: [nabla-hooks on PyPI](https://pypi.org/project/nabla-hooks/1.0.7/)
- Test: [nabla-hooks on Test PyPI](https://test.pypi.org/project/nabla-hooks/)

## [Test nabla-hooks as a developer](#table-of-contents)

### shell usage

Python example:

```python
from hooks import get_msg

match_msg
```

### versioneer

Using [versioneer](https://github.com/python-versioneer/python-versioneer) for version management:

```bash
versioneer install
# Check version
python setup.py version
python setup.py install
```

### Test

Using tox:

```bash
source deactivate
tox --notest
tox -e py  # Run tox using the version of Python in PATH
tox -e py312
```

Using pytest from the root directory:

```bash
pytest --cache-clear --setup-show hooks/tests/pytest_test.py
pytest --cache-clear --setup-show tests/test_package.py
```

### Poetry

Using [Poetry](https://python-poetry.org/) for dependency management:

```bash
poetry install
poetry env info
poetry shell
poetry run pytest
poetry build
# Configure PyPI token for publishing
poetry config pypi-token.pypi ${TWINE_PASSWORD}
# poetry publish --build
```

### Pdm

Using [PDM](https://pdm.fming.dev/) for dependency management:

```bash
pdm init
pdm run flake8
```

## [Update README.md](#table-of-contents)

Using [markdown-toc](https://github.com/jonschlinkert/markdown-toc) to update the table of contents:

```bash
npm install --save markdown-toc
markdown-toc README.md -i
markdown-toc CHANGELOG.md -i
```

With [pre-commit hooks](https://github.com/Lucas-C/pre-commit-hooks-nodejs):

```bash
pre-commit install
git add README.md
pre-commit run markdown-toc
```

Check markdown syntax with [remark-lint](https://github.com/remarkjs/remark-lint#cli):

```bash
npm run lint-md
```

## [npm-groovy-lint groovy formatting for Jenkinsfile](#table-of-contents)

Groovy linting and formatting for Jenkinsfile. Tested with Node.js 12 and 16 on Ubuntu 20 and 21 (not working with Node.js 11 and 14).

```bash
npm install -g npm-groovy-lint@8.2.0
npm-groovy-lint --format
ll .groovylintrc.json
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Add tests if applicable
5. Run pre-commit hooks and tests locally
6. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- [Issues](https://github.com/AlbanAndrieu/nabla-hooks/issues)
- [Gitter Chat](https://gitter.im/nabla-hooks/Lobby)

## Acknowledgments

This project uses several open-source tools and libraries. See [requirements.txt](requirements.txt) for the complete list.
