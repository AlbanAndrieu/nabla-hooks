#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

DEBUG=${DEBUG:=0}
[[ $DEBUG -eq 1 ]] && set -o xtrace

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./pre_commit_hooks/step-0-color.sh
source "${WORKING_DIR}/step-0-color.sh"

readonly MAX_NUMBER=2

echo 'Begin git'
echo -e "${green} Begin git check for ${MAX_NUMBER} branches. ${NC}"

if ! which git &>/dev/null; then
  >&2 echo -e "${red} ${double_arrow} git command not found. ${head_skull} ${NC}"
  exit 1
fi

git remote prune origin

count=$(git branch -r --merged | grep -v '\*\|master\|develop\|release' "$@" | wc -l)

if [ $count -gt ${MAX_NUMBER} ]; then
   echo -e "${red} ${double_arrow} You have more than ${MAX_NUMBER} branches ${reverse_exclamation} Please remove old stale branches from git ${head_skull} ${NC}"
   echo -e "${cyan} Find them ${happy_smiley}  doing : ${NC}"
   echo -e "${cyan} git branch -r --merged | grep -v '\*\|master\|develop\|release' ${NC}"
   # shellcheck disable=SC2006,SC2046
   for branch in $(git branch -r --merged | grep -v '\*\|master\|develop\|release' "$@"); do echo -e `git show --format="%ci %cr %an" $branch | head -n 1` \\t$branch; done | sort -r
   echo -e "${magenta} And delete them doing : ${NC}"
   echo -e "${magenta} git branch -d the_local_branch ${NC}"
   echo -e "${magenta} git push origin --delete the_remote_branch ${NC}"
fi

exit 0
