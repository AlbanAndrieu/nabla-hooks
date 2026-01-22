# GitHub Copilot Instructions for nabla-hooks

## Project Overview

**nabla-hooks** is a Python package that provides custom Git hooks for code quality validation. It integrates with the pre-commit framework and is intended for use by all Nabla products. The project is in maintenance mode, focusing on stability and bug fixes rather than new features.

**Primary Purpose**: Provide reusable pre-commit hooks for:
- Git branch validation (checking stale/merged branches)
- Jenkinsfile syntax validation
- Optional JIRA ticket validation in commit messages

## Tech Stack

- **Language**: Python 3.9+ (supports 3.9, 3.10, 3.11, 3.12)
- **Build System**: setuptools with versioneer
- **Dependency Management**: Poetry, Pipenv, or pip
- **Testing**: pytest with coverage
- **Linting**: flake8, pylint, ruff, black, mypy
- **Pre-commit Framework**: Hooks integrate with pre-commit
- **Shell Scripts**: Bash scripts for hook implementations
- **CI/CD**: GitHub Actions, GitLab CI, Travis CI

## Project Structure

```
nabla-hooks/
├── hooks/                      # Main Python package
│   ├── get_jira/              # JIRA integration modules
│   ├── get_msg.py             # Commit message handling
│   ├── get_repo.py            # Repository utilities
│   ├── commit-msg             # Git hook scripts
│   ├── pre-commit
│   ├── prepare-commit-msg
│   └── post-commit
├── pre_commit_hooks/          # Pre-commit hook scripts
│   ├── git-branches-check.sh
│   └── jenkinsfile-check.sh
├── tests/                     # Test suite
│   ├── test_*.py              # Python tests
│   └── unit/                  # Unit tests
├── docs/                      # Documentation
├── pyproject.toml             # Project configuration
├── setup.py                   # Package setup
├── tox.ini                    # Tox test configuration
└── .pre-commit-hooks.yaml     # Pre-commit hook definitions
```

## Essential Commands

### Development Setup
```bash
# Using Poetry (preferred for development)
poetry install
poetry shell

# Using Pipenv
pipenv install --dev
pipenv shell

# Using pip with virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests with pytest
pytest

# Run with coverage
pytest --cov=hooks --cov-report=xml --cov-report=html

# Run tests with tox (multiple Python versions)
tox

# Run specific test file
pytest tests/test_get_msg.py

# Run tests in verbose mode
pytest -v -s
```

### Linting and Code Quality
```bash
# Run flake8
flake8 --config .flake8 hooks/ tests/

# Run pylint
pylint hooks/ tests/

# Run mypy type checking
mypy hooks/

# Run black formatter
black hooks/ tests/

# Run ruff (fast linter)
ruff check hooks/ tests/

# Fix with ruff
ruff check --fix hooks/ tests/
```

### Pre-commit
```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run flake8 --all-files
```

### Building and Packaging
```bash
# Build package
python -m build

# Install package locally for testing
pip install -e .

# Clean build artifacts
make clean
# or
./clean.sh
```

## Code Style and Conventions

### Python Style
- **Line Length**: 88 characters (Black default)
- **Import Order**: Use isort with `multi_line_output = 3`
- **Type Hints**: Required for new code; use mypy for validation
- **Docstrings**: Use Google-style docstrings for public functions
- **Testing**: Maintain test coverage; use pytest for all tests

### Python Conventions
```python
# Use type hints
def get_user(user: str | None = None, verbose: bool = False) -> str:
    """Get username from parameter or environment.
    
    Args:
        user: Optional username override
        verbose: Enable verbose output
        
    Returns:
        The resolved username
    """
    pass

# Use f-strings for formatting
message = f"Processing branch: {branch_name}"

# Prefer Path over os.path
from pathlib import Path
config_path = Path(__file__).parent / "config.yaml"
```

### Shell Script Style
- Use bash (not sh)
- Add `set -euo pipefail` for safety
- Include descriptive comments
- Use colored output with termcolor/colorama where appropriate

### Commit Message Format
- Follow conventional commits format when possible
- Reference issue numbers: "fix: correct branch detection (#123)"
- Keep first line under 72 characters

## Git Workflow

- **Main Branch**: `master` (default branch)
- **Feature Branches**: Create from master, use descriptive names
- **Pull Requests**: Required for all changes
- **Pre-commit Hooks**: Must pass before commits
- **Code Review**: All PRs require review
- **CI**: GitHub Actions must pass (pytest, linting)

## Boundaries - What NOT to Touch

### Do Not Modify
- **Version files**: `hooks/_version.py` (managed by versioneer)
- **Lock files**: `poetry.lock`, `Pipfile.lock`, `package-lock.json`, `yarn.lock` (unless updating dependencies)
- **Build artifacts**: `dist/`, `build/`, `.eggs/`, `*.egg-info/`
- **CI configuration files**: Unless explicitly asked to modify CI
- **License file**: `LICENSE`
- **Vendored code**: Any third-party code in `lib/` or similar

### Restricted Areas
- **Security-sensitive code**: JIRA authentication, credential handling (requires extra scrutiny)
- **Core hook logic**: Changes to `hooks/commit-msg`, `hooks/pre-commit` scripts (high impact)
- **Production configurations**: Files in `etc/` (may affect deployments)

### Never Do
- Remove or disable existing tests (unless they're testing removed functionality)
- Add secrets, credentials, or API keys to the codebase
- Bypass pre-commit hooks or linting
- Make breaking API changes without discussion
- Change Python version requirements without discussion

## Testing Requirements

### Test Structure
- Tests in `tests/` directory mirror structure of `hooks/`
- Use pytest fixtures for common setup
- Mock external dependencies (JIRA API, git commands)
- Test both success and failure cases

### Test Examples
```python
# Use descriptive test names
def test_get_user_with_provided_user():
    """Test get_user returns the provided user."""
    user = get_user(user="testuser", verbose=False)
    assert user == "testuser"

# Use pytest fixtures
@pytest.fixture
def mock_git_repo(tmp_path):
    """Create a temporary git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    # ... setup code
    return repo_path

# Mock external calls
from unittest.mock import patch

@patch("hooks.get_jira.get_auth.os.environ.get")
def test_get_user_from_env(mock_environ_get):
    """Test get_user reads from environment."""
    mock_environ_get.return_value = "envuser"
    user = get_user(verbose=False)
    assert user == "envuser"
```

## Common Patterns

### Error Handling
```python
import sys
from typing import NoReturn

def exit_with_error(message: str, exit_code: int = 1) -> NoReturn:
    """Print error and exit."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(exit_code)
```

### Colored Output
```python
from colorama import init
from termcolor import colored

init()  # Initialize colorama for Windows support
print(colored("✓ Success", "green"))
print(colored("✗ Error", "red"))
```

### Git Operations
```python
import subprocess
from typing import List

def run_git_command(args: List[str]) -> str:
    """Run a git command and return output."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()
```

## Environment Variables

### Required for Testing
- `JIRA_USER`: JIRA username (optional, for JIRA tests)
- `JIRA_PASSWORD`: JIRA password (optional, for JIRA tests)
- `JIRA_URL`: JIRA instance URL (optional, for JIRA tests)
- `JENKINS_URL`: Jenkins URL (optional, for Jenkins validation tests)

### Git Configuration
Tests set these automatically:
- `GIT_CONFIG_COUNT`: Number of git config overrides
- `GIT_CONFIG_KEY_0`: `init.defaultBranch`
- `GIT_CONFIG_VALUE_0`: `master`

## Special Considerations

### Maintenance Mode
The project is in **maintenance mode**:
- Focus on bug fixes and security updates
- Avoid adding new features unless explicitly requested
- Keep changes minimal and backward-compatible
- Document any breaking changes clearly

### Python Version Support
- Support Python 3.9, 3.10, 3.11, and 3.12
- Test changes against all supported versions with tox
- Avoid using features only available in newer Python versions

### Pre-commit Integration
- Hooks must be defined in `.pre-commit-hooks.yaml`
- Entry points should be shell scripts in `pre_commit_hooks/`
- Scripts should exit with non-zero on failure
- Provide clear, actionable error messages

### Documentation
- Update `README.md` for user-facing changes
- Update `CONTRIBUTING.md` for development process changes
- Update docstrings for API changes
- Keep documentation concise and accurate

## Helpful Context

### When Working on Branch Checking
- Main logic in `pre_commit_hooks/git-branches-check.sh`
- Uses git commands to identify stale/merged branches
- Provides colored output for better UX

### When Working on JIRA Integration
- Code in `hooks/get_jira/` directory
- Authentication handled in `get_auth.py`
- JIRA API interaction requires credentials
- Support for cert-based authentication

### When Working on Commit Messages
- `hooks/get_msg.py` handles message parsing
- `hooks/prepare-commit-msg` is the git hook entry point
- Supports JIRA ticket detection and formatting

## Quick Reference

| Task | Command |
|------|---------|
| Run tests | `pytest` |
| Run specific test | `pytest tests/test_get_msg.py` |
| Check coverage | `pytest --cov=hooks` |
| Run linter | `flake8 hooks/` |
| Format code | `black hooks/ tests/` |
| Type check | `mypy hooks/` |
| Test all Python versions | `tox` |
| Install dev dependencies | `poetry install` |
| Run pre-commit checks | `pre-commit run --all-files` |
| Build package | `python -m build` |
| Clean artifacts | `make clean` |

## Questions to Ask Before Making Changes

1. **Does this change maintain backward compatibility?**
2. **Have I tested this with all supported Python versions?**
3. **Are there existing tests that cover this code path?**
4. **Does this change require documentation updates?**
5. **Will this work in CI environments (GitHub Actions, GitLab CI)?**
6. **Are there any security implications?**
7. **Is this change aligned with the maintenance mode status?**

---

**Remember**: This project is in maintenance mode. Keep changes minimal, focused, and well-tested. When in doubt, ask for clarification before making significant changes.
