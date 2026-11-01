<!-- markdown-link-check-disable-next-line -->

# [![Nabla](https://nabla.albandrieu.com/assets/nabla/nabla-4.png)](https://github.com/AlbanAndrieu) nabla-hooks

Nabla custom git hooks

[![License](http://img.shields.io/:license-apache-blue.svg?style=flat-square)](http://www.apache.org/licenses/LICENSE-2.0.html)
[![Gitter](https://badges.gitter.im/nabla-hooks/Lobby.svg)](https://gitter.im/nabla-hooks/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Python package](https://github.com/AlbanAndrieu/nabla-hooks/actions/workflows/python.yml/badge.svg)](https://github.com/AlbanAndrieu/nabla-hooks/actions/workflows/python.yml)

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

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](.github/CONTRIBUTING.md) for details on:

- Setting up your development environment with uv
- Running tests and code quality checks
- Submitting pull requests
- GitHub workflows and CI/CD

For issues, feature requests, or questions, please use our [GitHub issue templates](.github/ISSUE_TEMPLATE/).

# Table of contents

<!-- markdown-link-check-disable -->

// spell-checker:disable

<!-- toc -->

- [Initialize](#initialize)
  * [Development Setup](#development-setup)
  * [Requirements](#requirements)
    + [Runtime Requirements](#runtime-requirements)
  * [Install nabla-hooks as a developer](#install-nabla-hooks-as-a-developer)
  * [Install nabla-hooks to use it](#install-nabla-hooks-to-use-it)
    + [Using Pip](#using-pip)
    + [From Source](#from-source)
    + [Add .pre-commit-config.yaml in your git project](#add-pre-commit-configyaml-in-your-git-project)
    + [Using with OpenCommit (oco)](#using-with-opencommit-oco)
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
    + [uv](#uv)
- [Configure PyPI token for publishing](#configure-pypi-token-for-publishing)
- [Check pyproject.toml for errors](#check-pyprojecttoml-for-errors)
- [Lock dependencies without installing](#lock-dependencies-without-installing)
  * [GitHub Workflows and CI/CD](#github-workflows-and-cicd)
    + [Available Workflows](#available-workflows)
    + [Workflow Requirements](#workflow-requirements)
    + [Local CI Simulation](#local-ci-simulation)
  * [Update README.md](#update-readmemd)
  * [npm-groovy-lint groovy formatting for Jenkinsfile](#npm-groovy-lint-groovy-formatting-for-jenkinsfile)
  * [Contributing](#contributing)
  * [License](#license)
  * [Support](#support)
  * [Acknowledgments](#acknowledgments)

<!-- tocstop -->

// spell-checker:enable

<!-- markdown-link-check-enable -->

# [Initialize](#table-of-contents)

## Development Setup

See [ONBOARDING.md](ONBOARDING.md) (mise + uv):

```bash
mise install
uv sync
pre-commit install
```

## [Requirements](#table-of-contents)

### Runtime Requirements

This package requires the following to run:

- Python >= 3.13
- [pre-commit](http://pre-commit.com)
- [jira](https://pypi.org/project/jira/) (optional, for JIRA integration)

See `pyproject.toml` (locked in `uv.lock`) for the complete list of Python dependencies.

## [Install nabla-hooks as a developer](#table-of-contents)

Python comes from `mise.toml`, dependencies from `uv.lock`; `direnv` activates `.venv`:

```bash
mise install
uv sync
uvx pip-audit  # dependency vulnerability audit
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
      - id: jira-check  # Validates commit messages contain JIRA tickets
        stages: [commit-msg]
      # or, for GitHub Issues:
      # - id: github-issue-check
```

**GitHub Issue Check Hook**: Validates that commit messages reference a GitHub issue: `#123`, `owner/repo#123` or `GH-123`. Git comment lines are ignored. To accept both trackers, use `jira-check` with `args: [--tracker, any]`.

The `get_msg` prepare-commit-msg helper also reads the issue from the branch name:

- `feature/PROJ-123`: JIRA, as before.
- `feature/123-add-login`, `fix/GH-123` or `issue-123`: GitHub. It checks the issue with `gh issue view` (run `gh auth login` first), refuses closed issues (exit 3) and prefixes the message with `GH-123 : `. It uses `GH-` rather than `#` because git drops lines starting with `#`. Disable it with `--no-github` or `NABLA_GITHUB_ISSUES=false`.
- `alban/eng-123-add-login` (Linear's default branch name) or `feature/ENG-123`: Linear, opt-in with `--linear` or `NABLA_LINEAR_ISSUES=true` because Linear and JIRA keys look alike. It checks the issue with the Linear API (`LINEAR_API_KEY`, a personal API key), refuses completed or canceled issues (exit 3) and prefixes the message with `ENG-123 : `, which Linear's GitHub integration links to the issue. To only require a Linear key in the message, `jira-check` already matches it.

**JIRA Check Hook**: Validates that commit messages contain JIRA ticket references (e.g., PROJ-123, TEST-456).

Features:
- Pattern matching: `[A-Z]{2,10}-[0-9]+` (customizable via `--pattern`)
- Auto-skips merge, revert, fixup, and squash commits
- No JIRA API access required - simple pattern validation
- User-friendly error messages with examples

Example valid commit messages:
- `PROJ-123 Add new feature`
- `[TEAM-456] Fix critical bug`
- `ABC-789: Update documentation`

Testing locally

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
    -   id: jira-check
        name: JIRA ticket validation
        entry: hooks/validate_jira.py
        language: python
        stages: [commit-msg]
```

Test locally:

```bash
pre-commit try-repo . git-branches-check --verbose
```

2. Install pre-commit hooks in your repository

For commit-msg hooks (like JIRA check), also run:
`pre-commit install --hook-type commit-msg`

3. enjoy it

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

### Using with OpenCommit (oco)

This project now supports [OpenCommit](https://github.com/di-sukharev/opencommit), an AI-powered tool that generates commit messages automatically.

#### Setup OpenCommit

1. Install OpenCommit globally:

```bash
npm install -g opencommit
# or use it with npx
npx opencommit
```

2. Configure your AI provider (OpenAI, Claude, or local models via Ollama):

```bash
oco config set OCO_API_KEY=<your_api_key>
# For local models with Ollama:
# oco config set OCO_AI_PROVIDER=ollama
# oco config set OCO_MODEL=llama3:8b
```

3. Install as a git hook (optional, if you want AI-generated messages by default):

```bash
oco hook set
```

#### Using OpenCommit with nabla-hooks

The nabla-hooks `prepare-commit-msg` hook is now compatible with OpenCommit:

- **With OpenCommit hook installed**: When you run `git commit`, OpenCommit will generate a commit message, and nabla-hooks will validate it.
- **Manual AI generation**: You can use `oco` command directly to generate and commit:

```bash
git add .
oco
```

- **Fallback to commitizen**: If no commit message is provided, the hook will fallback to using commitizen for message generation.

The hook intelligently detects existing commit messages (from oco, manual entry, or other tools) and validates them without forcing regeneration.

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

### uv

# Configure PyPI token for publishing
export UV_PUBLISH_TOKEN=${TWINE_PASSWORD}
uv build && uv publish

# Check pyproject.toml for errors
uv lock --check

# Lock dependencies without installing
uv lock
```

For more details, see the [CONTRIBUTING.md](.github/CONTRIBUTING.md) guide.

### Pdm

Using [PDM](https://pdm.fming.dev/) for dependency management:

```bash
pdm init
pdm run flake8
```

## [GitHub Workflows and CI/CD](#table-of-contents)

This project uses GitHub Actions for continuous integration and deployment. The following workflows are configured:

### Available Workflows

1. **Python Package** (`.github/workflows/python.yml`)
   - Runs on: Push to master, Pull requests
   - Tests on: Python 3.13, 3.14 and 3.15
   - Steps: Lint (flake8, pylint, bandit), Test (pytest, tox)
   - Badge: ![Python package](https://github.com/AlbanAndrieu/nabla-hooks/actions/workflows/python.yml/badge.svg)

2. **CodeQL Analysis** (`.github/workflows/codeql.yml`)
   - Security scanning for code vulnerabilities
   - Runs on: Push and Pull requests

3. **Linter** (`.github/workflows/linter.yml`)
   - Comprehensive linting across the project
   - Uses MegaLinter for multiple file types

4. **Publish** (`.github/workflows/pythonpublish.yml`)
   - `uv build` + `uv publish` on release

### Workflow Requirements

All pull requests must pass:
- ✅ Linting (flake8, pylint, bandit)
- ✅ Tests (pytest with >30% coverage)
- ✅ Code quality checks (SonarCloud)
- ✅ Security scanning (CodeQL)

### Local CI Simulation

Before pushing, run the same checks locally:

```bash
# Activate the uv environment
source .venv/bin/activate

# Run linters
uv run flake8 hooks tests
uv run pylint hooks
uv run bandit -r hooks

# Run tests
uv run pytest --cov=hooks --cov-fail-under=30

# Run pre-commit hooks
uv run pre-commit run --all-files
```

For more details, see [CONTRIBUTING.md](.github/CONTRIBUTING.md).

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

This project uses several open-source tools and libraries. See [pyproject.toml](pyproject.toml) for the complete list.
