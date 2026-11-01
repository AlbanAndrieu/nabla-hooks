# Quick Reference Guide

## uv Cheat Sheet

### Installation and Setup
```bash
# Install uv
mise install

# Install project dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate
```

### Dependency Management
```bash
# Add a dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Remove a dependency
uv remove package-name

# Update dependencies
uv lock --upgrade

# Show installed packages
uv pip list

# Show dependency tree
uv tree
```

### Running Commands
```bash
# Run command in virtual environment
uv run <command>

# Run Python script
uv run python script.py

# Run pytest
uv run pytest

# Run pre-commit
uv run pre-commit run --all-files
```

### Build and Publish
```bash
# Build package
uv build

# Check package
uv lock --check

# Publish to PyPI
uv publish
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
uv sync

# 4. Install pre-commit
uv run pre-commit install

# 5. Run tests to verify
uv run pytest
```

### Daily Development
```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes

# 3. Run checks
uv run pre-commit run --all-files
uv run pytest

# 4. Commit and push
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature
```

## Testing Commands

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=hooks --cov-report=html

# Run specific test file
uv run pytest tests/test_package.py

# Run tests verbosely
uv run pytest -v

# Run with multiple Python versions
uv run tox
```

## Code Quality Commands

```bash
# Format code
uv run black hooks tests

# Lint with flake8
uv run flake8 hooks tests

# Lint with pylint
uv run pylint hooks

# Type check with mypy
uv run mypy hooks

# Security scan
uv run bandit -r hooks

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

## Common Issues and Solutions

### uv Not Found
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Lock File Issues
```bash
# Update lock file
uv lock

# Reinstall
uv sync
```

### Virtual Environment Issues
```bash
# Show environment info
uv python find

# Remove environment
rm -rf .venv

# Recreate environment
uv sync
```

### Pre-commit Hook Failures
```bash
# Update hooks
uv run pre-commit autoupdate

# Clean and reinstall
uv run pre-commit clean
uv run pre-commit install
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
├── pyproject.toml       # project configuration (uv)
├── README.md           # Project README
└── .pre-commit-config.yaml  # Pre-commit config
```

## Useful Links

- [uv Documentation](https://docs.astral.sh/uv/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Commitizen](https://commitizen-tools.github.io/commitizen/)

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/AlbanAndrieu/nabla-hooks/issues)
- **Chat**: [Gitter](https://gitter.im/nabla-hooks/Lobby)
- **Documentation**: [README.md](../README.md), [CONTRIBUTING.md](CONTRIBUTING.md)
