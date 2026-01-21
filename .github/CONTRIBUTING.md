# Contributing to nabla-hooks

Thank you for your interest in contributing to nabla-hooks! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
  - [Making Changes](#making-changes)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
- [Submitting Changes](#submitting-changes)
  - [Pull Request Process](#pull-request-process)
  - [Commit Message Guidelines](#commit-message-guidelines)
- [GitHub Workflows](#github-workflows)
- [Getting Help](#getting-help)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9 or higher (3.12+ recommended for development)
- [Poetry](https://python-poetry.org/docs/#installation) 2.0+
- Git
- Pre-commit (will be installed via Poetry)

### Development Setup

1. **Fork the repository** on GitHub and clone your fork locally:

   ```bash
   git clone https://github.com/YOUR_USERNAME/nabla-hooks.git
   cd nabla-hooks
   ```

2. **Set up Python environment** using pyenv (recommended):

   ```bash
   # Install pyenv if not already installed
   curl -L https://pyenv.run | bash
   
   # Install Python 3.12
   pyenv install 3.12.10
   pyenv local 3.12.10
   ```

3. **Install dependencies using Poetry**:

   ```bash
   # Install Poetry if not already installed
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install project dependencies
   poetry install
   
   # Activate the virtual environment
   poetry shell
   ```

4. **Install pre-commit hooks**:

   ```bash
   poetry run pre-commit install
   ```

5. **Verify installation**:

   ```bash
   poetry run pytest tests/
   ```

## Development Workflow

### Making Changes

1. **Create a new branch** for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes** following the project's coding standards:
   - Follow PEP 8 style guidelines
   - Add tests for new functionality
   - Update documentation as needed
   - Keep changes focused and atomic

3. **Run pre-commit checks** before committing:

   ```bash
   poetry run pre-commit run --all-files
   ```

### Running Tests

Run the test suite to ensure your changes don't break existing functionality:

```bash
# Run all tests with pytest
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=hooks --cov-report=html

# Run specific test file
poetry run pytest tests/test_package.py

# Run tests with tox (multiple Python versions)
poetry run tox
```

### Code Quality

Maintain code quality by running the following tools:

```bash
# Format code with Black
poetry run black hooks tests

# Lint with flake8
poetry run flake8 hooks tests --config .flake8

# Lint with pylint
poetry run pylint hooks

# Type checking with mypy
poetry run mypy hooks

# Security scanning with bandit
poetry run bandit -r hooks

# Run all linters
./scripts/run-pylint.sh
./scripts/run-bandit.sh
```

## Submitting Changes

### Pull Request Process

1. **Update your branch** with the latest changes from master:

   ```bash
   git checkout master
   git pull upstream master
   git checkout your-branch-name
   git rebase master
   ```

2. **Push your changes** to your fork:

   ```bash
   git push origin your-branch-name
   ```

3. **Create a Pull Request** on GitHub:
   - Use a clear and descriptive title
   - Fill out the PR template completely
   - Link any related issues
   - Add appropriate labels
   - Request review from maintainers

4. **Address review feedback**:
   - Make requested changes in new commits
   - Push updates to your branch
   - Respond to comments professionally

5. **After approval**, a maintainer will merge your PR

### Commit Message Guidelines

This project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) for standardized commit messages. Follow these guidelines:

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Other changes

**Examples:**
```
feat: add support for Python 3.13

Implement Python 3.13 compatibility and update dependencies.

Closes #123
```

```
fix: resolve git branch detection issue

Fix bug where branch names with special characters were not properly detected.

Fixes #456
```

## GitHub Workflows

This project uses GitHub Actions for continuous integration. The following workflows run automatically:

- **Python package** (`python.yml`): Runs tests on all supported Python versions (currently 3.9–3.13)
- **CodeQL Analysis** (`codeql.yml`): Security scanning
- **Linting** (`linter.yml`): Code quality checks
- **Release** (`release.yml`): Automated releases
- **Dependabot**: Dependency updates

All workflows must pass before a PR can be merged.

## Project Structure

```
nabla-hooks/
├── .github/              # GitHub configuration
│   ├── workflows/       # GitHub Actions workflows
│   ├── ISSUE_TEMPLATE/  # Issue templates
│   └── CONTRIBUTING.md  # This file
├── hooks/               # Main package code
├── pre_commit_hooks/    # Pre-commit hook scripts
├── tests/               # Test files
├── docs/                # Documentation
├── pyproject.toml       # Poetry configuration and dependencies
├── README.md           # Project overview
└── .pre-commit-config.yaml  # Pre-commit configuration
```

## Poetry Commands Reference

```bash
# Install dependencies
poetry install

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Show installed packages
poetry show

# Build the package
poetry build

# Publish to PyPI
poetry publish

# Run a command in the virtual environment
poetry run command

# Activate the virtual environment
poetry shell

# Check pyproject.toml validity
poetry check

# Lock dependencies without installing
poetry lock
```

## Getting Help

If you need help or have questions:

- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Gitter**: Join our [Gitter chat](https://gitter.im/nabla-hooks/Lobby)
- **Documentation**: Check the [README.md](../README.md) and [docs/](../docs/)

## License

By contributing to nabla-hooks, you agree that your contributions will be licensed under the Apache License 2.0.

Thank you for contributing! 🎉
