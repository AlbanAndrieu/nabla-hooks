# Contributing to nabla-hooks

First off, thank you for considering contributing to nabla-hooks! It's people like you that make nabla-hooks such a great tool.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be kind and courteous to others.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment tool (venv, virtualenv, or pyenv)

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/nabla-hooks.git
cd nabla-hooks
```

2. **Set up your development environment**

Using pyenv and pipenv:

```bash
# Install Python 3.12
pyenv install 3.12.10
pyenv local 3.12.10

# Install dependencies
python -m pipenv install --dev --ignore-pipfile

# Activate virtual environment
pipenv shell
```

Using poetry:

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

3. **Install pre-commit hooks**

```bash
pre-commit install
```

4. **Verify your setup**

```bash
# Run tests
pytest

# Run linters
make lint
```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Code samples** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why is this enhancement needed?
- **Proposed solution**
- **Alternatives considered**

### Pull Requests

1. **Create a branch** from `main` for your changes

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

2. **Make your changes**
   - Write clear, concise commit messages
   - Follow the style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**

```bash
# Run tests
pytest

# Run linters
ruff check .
black --check .

# Run pre-commit checks
pre-commit run --all-files
```

4. **Commit your changes**

```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve issue with X"
```

Use conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

5. **Push to your fork**

```bash
git push origin feature/your-feature-name
```

6. **Open a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Explain what changes you made and why

## Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 88)
- Use [Ruff](https://docs.astral.sh/ruff/) for linting
- Write docstrings for all public functions and classes

Example:

```python
def validate_commit_message(message: str) -> bool:
    """
    Validate commit message format.

    Args:
        message: The commit message to validate

    Returns:
        True if valid, False otherwise
    """
    # Implementation
    pass
```

### Shell Script Style

- Follow [ShellCheck](https://www.shellcheck.net/) recommendations
- Use bash for shell scripts
- Include shebang: `#!/usr/bin/env bash`
- Add comments for complex logic

### Documentation Style

- Use Markdown for documentation
- Follow existing structure
- Include code examples
- Keep line length reasonable (80-100 characters)
- Run markdown linters

### Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Example:
```
feat(hooks): add git-branches-check hook

Add a new pre-commit hook that checks for stale branches.
This helps keep repositories clean by identifying old branches.

Closes #123
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_package.py

# Run with coverage
pytest --cov=hooks --cov=pre_commit_hooks

# Run specific test
pytest tests/test_package.py::test_function_name
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Include docstrings for complex tests
- Use fixtures for common setup

Example:

```python
def test_validate_commit_message_with_valid_format():
    """Test that valid commit messages pass validation."""
    message = "feat: add new feature"
    assert validate_commit_message(message) is True
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Test both success and failure paths

## Submitting Changes

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] Pre-commit hooks pass
- [ ] No merge conflicts with main branch

### Pull Request Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, maintainers will merge your PR

### After Your PR is Merged

- Delete your feature branch
- Update your local repository
- Celebrate! 🎉

## Development Tools

### Useful Make Commands

```bash
make install    # Install dependencies
make test       # Run tests
make lint       # Run linters
make format     # Format code
make clean      # Clean build artifacts
```

### Useful Git Commands

```bash
# Update your fork
git remote add upstream https://github.com/AlbanAndrieu/nabla-hooks.git
git fetch upstream
git merge upstream/main

# Squash commits
git rebase -i HEAD~N  # where N is number of commits
```

## Getting Help

- [GitHub Issues](https://github.com/AlbanAndrieu/nabla-hooks/issues)
- [Gitter Chat](https://gitter.im/nabla-hooks/Lobby)
- [Documentation](https://github.com/AlbanAndrieu/nabla-hooks#readme)

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes (for significant contributions)
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

Thank you for your contributions! 🙏
