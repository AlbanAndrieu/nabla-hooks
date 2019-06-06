#!/bin/bash

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

unset SHELLCHECK_OPTS

which shellcheck &> /dev/null
if [[ $? != 0 ]]; then
    echo "are you sure you have installed shellcheck?"
    exit 1
fi

cat << EOS > ${WORKING_DIR}/.pre-commit-config.yaml
-   repo: https://github.com/detailyang/pre-commit-shell
    sha: master
    hooks:
    -   id: shell-lint
-   repo: $(pwd)
    sha: $(git rev-parse HEAD)
    hooks:
    -   id: git-branches-check
        name: Git branches check
        description: Check for old stale and already merged branches from the current repo with user friendly messages and colors
        entry: pre_commit_hooks/git-branches-check.sh
        language: script
        types: [shell]
        always_run: true
        verbose: true
        additional_dependencies: [jira>=2.0.0]
EOS

tmpdir=$(mktemp -t pre-commit-shell.XXXXXX  -d)
cp test/test.sh "$tmpdir"
cp test/.pre-commit-config.yaml "$tmpdir"
pushd "$tmpdir"
pwd
git init
git config user.email "alban.andrieu@free.fr"
git config user.name "aandrieu"
pre-commit install
git add .pre-commit-config.yaml; git commit -a -m "init test case"
git add . --all
tmpfile=$(mktemp -t pre-commit-shell.XXX)
git commit -a -m "let begin test" &> "$tmpfile"
#echo "less $tmpfile"
popd

function passed() {
    echo "$@"
    rm -rf "$tmpdir"

    return 0
}

function failed() {
    echo "$@"
    exit 255
}

grep --quiet "SC2115" $tmpfile && passed "SC2115 PASSED" || failed "SC2115 FAILED"
grep --quiet "SC2086" $tmpfile && passed "SC2086 PASSED" || failed "SC2086 FAILED"
grep --quiet "SC2034" $tmpfile && passed "SC2034 PASSED" || failed "SC2034 FAILED"
