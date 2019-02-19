#!/usr/bin/env bash
set -xv

set -o errexit
set -o pipefail
set -o nounset

DEBUG=${DEBUG:=0}
[[ $DEBUG -eq 1 ]] && set -o xtrace

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

# shellcheck source=./pre_commit_hooks/step-0-color.sh
source "${WORKING_DIR}/step-0-color.sh"

# You can test it with
# pre_commit_hooks/git-branches-check.sh -m 10
# pre_commit_hooks/git-branches-check.sh --max 10 --verbose

usage() { echo "Usage: $0 [-m|--max <10>] []" 1>&2; exit 1; }

# shellcheck disable=SC2006
TEMP=`getopt -o vdm: --long verbose,debug,max:,debugfile:,branches:  -- "$@"`

# shellcheck disable=SC2181
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

# Note the quotes around `$TEMP': they are essential!
eval set -- "$TEMP"

VERBOSE=false
DEBUG=false
MAX_NUMBER=2
DEBUGFILE=
BRANCH='\*\|master\|develop\|release'
while true; do
  case "$1" in
    -v | --verbose ) VERBOSE=true; shift ;;
    -d | --debug ) DEBUG=true; shift ;;
    -m | --max ) MAX_NUMBER="$2"; shift 2 ;;
    --branches )
      BRANCH="$2"; shift 2 ;;
    -- ) shift; break ;;
    * ) usage ;;
  esac
done

if ${VERBOSE}; then
  echo -e "${green} Begin git check for ${MAX_NUMBER} branches ${BRANCH}. ${NC}"
fi

if ! which git &>/dev/null; then
  >&2 echo -e "${red} ${double_arrow} git command not found. ${head_skull} ${NC}"
  exit 1
fi


git remote prune origin || true

count=$(git branch -r --merged | grep -c -v ${BRANCH} || true)

if [[ -f ${DEBUGFILE} ]]; then
   git branch -r --merged | grep -c -v ${BRANCH} > ${DEBUGFILE} 2>&1
fi

if [ $count -gt ${MAX_NUMBER} ]; then
   echo -e "${red} ${double_arrow} You have more than ${MAX_NUMBER} branches ${reverse_exclamation} Please remove old stale branches from git ${head_skull} ${NC}"
   echo -e "${cyan} Find them ${happy_smiley}  doing : ${NC}"
   echo -e "${cyan} git branch -r --merged | grep -v ${BRANCH} ${NC}"
   # shellcheck disable=SC2006,SC2046
   for branch in $(git branch -r --merged | grep -v ${BRANCH}); do echo -e `git show --format="%ci %cr %an" $branch | head -n 1` \\t$branch; done | sort -r
   echo -e "${magenta} And delete them doing : ${NC}"
   echo -e "${magenta} git branch -d the_local_branch ${NC}"
   echo -e "${magenta} git push origin --delete the_remote_branch ${NC}"
fi

exit 0
