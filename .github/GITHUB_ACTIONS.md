# GitHub Actions and CI/CD

This document provides an overview of the continuous integration and deployment workflows for nabla-hooks.

## Workflow Overview

All workflows are located in `.github/workflows/` and run automatically on relevant events.

## Active Workflows

### 1. Python Package (`python.yml`)

**Purpose**: Main CI workflow for testing and linting

**Triggers**:
- Push to `master` branch
- Pull requests

**Matrix**:
- Python versions: 3.13, 3.14, 3.15
- OS: Ubuntu Latest

**Steps**:
1. Checkout code
2. Set up Python environment
3. Install dependencies (uv)
4. Lint with flake8
5. Lint with pylint
6. Security scan with bandit
7. Test with pytest (requires >30% coverage)
8. Test with tox

**Status**: ![Python package](https://github.com/AlbanAndrieu/nabla-hooks/actions/workflows/python.yml/badge.svg)

### 2. CodeQL Analysis (`codeql.yml`)

**Purpose**: Security vulnerability scanning

**Triggers**:
- Push to main branches
- Pull requests
- Scheduled (weekly)

**Languages**: Python, JavaScript

**Status**: Runs automatically for security analysis

### 3. Linter (`linter.yml`)

**Purpose**: Comprehensive code quality checks using MegaLinter

**Triggers**:
- Push events
- Pull requests

**Linters**: Multiple linters for Python, YAML, Markdown, Shell, and more

### 4. PyPI Publish (`pythonpublish.yml`)

**Purpose**: Build and publish the package to PyPI with `uv build` + `uv publish`

**Triggers**:
- Release creation

## Required Checks for PRs

Before a PR can be merged, it must pass:

- ✅ Python package workflow (all Python versions)
- ✅ Linter checks
- ✅ CodeQL security scan
- ✅ Test coverage (minimum 30%)
- ✅ Pre-commit hooks

## Running Workflows Locally

### Prerequisites

```bash
# Install dependencies
uv sync

# Install pre-commit
uv run pre-commit install
```

### Simulate CI Checks

```bash
# Run flake8
uv run flake8 hooks tests --config .flake8

# Run pylint
uv run pylint hooks

# Run bandit
uv run bandit -r hooks

# Run pytest with coverage
uv run pytest --cov=hooks --cov-fail-under=30 --junit-xml=junit.xml

# Run tox (all Python versions)
uv run tox

# Run pre-commit hooks
uv run pre-commit run --all-files
```

## Workflow Files

| Workflow | File | Status |
|----------|------|--------|
| Python Package | `.github/workflows/python.yml` | Active |
| CodeQL | `.github/workflows/codeql.yml` | Active |
| Linter | `.github/workflows/linter.yml` | Active |
| PyPI Publish | `.github/workflows/pythonpublish.yml` | Active |

## Secrets Required

The following GitHub secrets are required for workflows:

- `SONAR_TOKEN`: SonarCloud authentication
- `TWINE_PASSWORD`: PyPI authentication token
- `TRUNK_API_TOKEN`: Trunk.io integration (optional)

## Troubleshooting

### Workflow Failures

1. **Linting Errors**: Run `uv run flake8` and `uv run pylint` locally
2. **Test Failures**: Run `uv run pytest -v` to see detailed output
3. **Coverage Too Low**: Add more tests or adjust coverage threshold
4. **Security Issues**: Review CodeQL or Bandit reports

### Common Issues

**uv Lock Issues**:
```bash
uv lock
uv sync
```

**Pre-commit Hook Failures**:
```bash
uv run pre-commit run --all-files
```

**Dependency Conflicts**:
```bash
uv lock --upgrade
uv lock
```

## Contributing

For more information on contributing and working with these workflows, see:
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [README.md](../README.md)

## Support

If you encounter issues with CI/CD:
1. Check workflow logs in GitHub Actions tab
2. Open an issue using the bug report template
3. Join our Gitter chat for real-time help
