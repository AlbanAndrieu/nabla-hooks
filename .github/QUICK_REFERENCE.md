# Quick Reference Guide

## Poetry Cheat Sheet

### Installation and Setup
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Dependency Management
```bash
# Add a dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name

# Remove a dependency
poetry remove package-name

# Update dependencies
poetry update

# Show installed packages
poetry show

# Show dependency tree
poetry show --tree
```

### Running Commands
```bash
# Run command in virtual environment
poetry run <command>

# Run Python script
poetry run python script.py

# Run pytest
poetry run pytest

# Run pre-commit
poetry run pre-commit run --all-files
```

### Build and Publish
```bash
# Build package
poetry build

# Check package
poetry check

# Publish to PyPI
poetry publish
```

## Development Workflow

### First Time Setup
```bash
# 1. Clone and enter repo
git clone https://github.com/AlbanAndrieu/nabla-hooks.git
cd nabla-hooks

# 2. Set Python version
pyenv install 3.12.10
pyenv local 3.12.10

# 3. Install dependencies
poetry install

# 4. Install pre-commit
poetry run pre-commit install

# 5. Run tests to verify
poetry run pytest
```

### Daily Development
```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes

# 3. Run checks
poetry run pre-commit run --all-files
poetry run pytest

# 4. Commit and push
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature
```

## Testing Commands

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=hooks --cov-report=html

# Run specific test file
poetry run pytest tests/test_package.py

# Run tests verbosely
poetry run pytest -v

# Run with multiple Python versions
poetry run tox
```

## Code Quality Commands

```bash
# Format code
poetry run black hooks tests

# Lint with flake8
poetry run flake8 hooks tests

# Lint with pylint
poetry run pylint hooks

# Type check with mypy
poetry run mypy hooks

# Security scan
poetry run bandit -r hooks

# Run all pre-commit hooks
poetry run pre-commit run --all-files
```

## Common Issues and Solutions

### Poetry Not Found
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Lock File Issues
```bash
# Update lock file
poetry lock --no-update

# Reinstall
poetry install
```

### Virtual Environment Issues
```bash
# Show environment info
poetry env info

# Remove environment
poetry env remove python

# Recreate environment
poetry install
```

### Pre-commit Hook Failures
```bash
# Update hooks
poetry run pre-commit autoupdate

# Clean and reinstall
poetry run pre-commit clean
poetry run pre-commit install
```

## Git Commands

### Branch Management
```bash
# Create new branch
git checkout -b feature/my-feature

# Update from master
git checkout master
git pull origin master
git checkout feature/my-feature
git rebase master

# Push changes
git push origin feature/my-feature
```

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, perf, test, build, ci, chore

**Examples**:
```
feat: add new validation hook
fix: resolve branch detection bug
docs: update installation instructions
```

## Project Structure

```
nabla-hooks/
├── .github/              # GitHub config (workflows, templates)
├── hooks/               # Main package source code
├── pre_commit_hooks/    # Pre-commit hook scripts
├── tests/               # Test files
├── docs/                # Documentation
├── pyproject.toml       # Poetry configuration
├── README.md           # Project README
└── .pre-commit-config.yaml  # Pre-commit config
```

## Useful Links

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/AlbanAndrieu/nabla-hooks/issues)
- **Chat**: [Gitter](https://gitter.im/nabla-hooks/Lobby)
- **Documentation**: [README.md](../README.md), [CONTRIBUTING.md](CONTRIBUTING.md)
