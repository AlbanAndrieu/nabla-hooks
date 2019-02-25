#! /bin/bash

WORKING_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" && pwd  )"

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
popd
rm -rf "$tmpdir"

function passed() {
    echo "$@"

    return 0
}

function failed() {
    echo "$@"
    exit 255
}

grep --quiet "SC2115" $tmpfile && passed "SC2115 PASSED" || failed "SC2115 FAILED"
grep --quiet "SC2086" $tmpfile && passed "SC2086 PASSED" || failed "SC2086 FAILED"
grep --quiet "SC2034" $tmpfile && passed "SC2034 PASSED" || failed "SC2034 FAILED"
