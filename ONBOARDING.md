# Onboarding

## Workstation

The workstation is rebuilt from three repositories:

| Repository | Role |
|---|---|
| [dotfiles](https://github.com/AlbanAndrieu/dotfiles) | Dotfiles (`~/.bashrc`, `~/.config/...`), global mise config |
| [nabla](https://github.com/AlbanAndrieu/nabla) | Shell environment: [`env/home/dev.env.sh`](https://github.com/AlbanAndrieu/nabla/blob/master/env/home/dev.env.sh) sets variables and `PATH`, sourced by `~/.bashrc` |
| nabla-hooks (this repo) | Git hooks, project runtimes (`mise.toml`) and Python deps (`uv.lock`) |

Legacy version managers are off by default in `dev.env.sh`; mise owns node, python and go.
Re-enable one only if needed:

```bash
export NABLA_NVM_SHELL_INTEGRATION=on    # nvm
export NABLA_PYENV_SHELL_INTEGRATION=on  # pyenv
export NABLA_GVM_SHELL_INTEGRATION=on    # gvm
```

Git identity comes from `~/.gitconfig` (dotfiles) and its `includeIf` rules; `dev.env.sh`
does not export `GIT_AUTHOR_*`.

## Runtimes (mise)

Versions are pinned in `mise.toml` (node, python, uv, terragrunt, ...).

```bash
mise install
```

## JavaScript tools (npm)

Lint/format tools are pinned in `package.json` and updated by Renovate.

```bash
npm ci
npx biome check .
npx remark .
```

## Python

```bash
uv sync
pre-commit install
pre-commit run --all-files
```

## Claude Code

Use the native installer (independent of the Node version):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```
