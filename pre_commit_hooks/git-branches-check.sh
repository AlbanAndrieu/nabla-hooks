#!/usr/bin/env bash
set -euo pipefail

[[ "${DEBUG:-0}" == "1" ]] && set -o xtrace

WORKING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=./pre_commit_hooks/step-0-color.sh
source "${WORKING_DIR}/step-0-color.sh"

# You can test it with
# pre_commit_hooks/git-branches-check.sh -m 10
# pre_commit_hooks/git-branches-check.sh --max=1 --verbose
# DEBUG=1 pre_commit_hooks/git-branches-check.sh

usage() {
  echo "Usage: $0 [-v|--verbose] [-d|--debug] [-m|--max <2>] [--branches <regex of branches to keep>]" 1>&2
  exit 1
}

VERBOSE=false
MAX_NUMBER=2
BRANCH="TODO|main|master|develop|release|HEAD"

# Hand-written parsing: macOS getopt has no long options.
while [[ $# -gt 0 ]]; do
  case "$1" in
  -v | --verbose) VERBOSE=true ;;
  -d | --debug) set -o xtrace ;;
  -m | --max)
    MAX_NUMBER="${2:?}"
    shift
    ;;
  --max=*) MAX_NUMBER="${1#*=}" ;;
  --branches)
    BRANCH="${2:?}"
    shift
    ;;
  --branches=*) BRANCH="${1#*=}" ;;
  -h | --help) usage ;;
  *) ;; # pre-commit passes file names
  esac
  shift
done

if ! command -v git &>/dev/null; then
  echo >&2 -e "${red} ${double_arrow} git command not found. ${head_skull} ${NC}"
  exit 1
fi

GIT_USERNAME=${GIT_USERNAME:-$(git config user.name || true)}

if ${VERBOSE}; then
  echo -e "${green} Begin git check for ${MAX_NUMBER} branches ${BRANCH} for user \"${GIT_USERNAME}\". ${NC}"
fi

git fetch --prune >/dev/null 2>&1 || true

# One git call: merged remote branches, newest first, minus the ones to keep.
stale=$(git for-each-ref --merged=HEAD --sort=-committerdate \
  --format='%(committerdate:iso) %(committerdate:relative) %(authorname)%09%(refname:lstrip=2)' refs/remotes |
  awk -F'\t' -v keep="${BRANCH}" '$2 !~ keep')
count=$(grep -c . <<<"${stale}" || true)

if [ "${count}" -gt "${MAX_NUMBER}" ]; then
  echo -e "${red} ${double_arrow} You have more than ${MAX_NUMBER} branches ${reverse_exclamation} Please remove old stale branches from git ${head_skull} ${NC}"
  echo -e "${cyan} Yours ${happy_smiley} : ${NC}"
  grep -F "${GIT_USERNAME}" <<<"${stale}" || true
  echo -e "${magenta} And delete them doing : ${NC}"
  echo -e "${magenta} git branch -d the_local_branch ${NC}"
  echo -e "${magenta} git push origin --delete the_remote_branch ${NC}"
fi
