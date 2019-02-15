# nabla-hooks

Nabla custom git hooks

This project intend to be uses by all Nabla products

## Quality tools

### python 3.6

Install python 3.6 and virtualenv

`virtualenv --no-site-packages /opt/ansible/env36 -p python3.6`

`source /opt/ansible/env36/bin/activate`

`pip install -r requirements-current-3.6.txt`

### pre-commit

See [pre-commit](http://pre-commit.com/)
Run `pre-commit install`

Run `pre-commit run --all-files`

Run `SKIP=flake8 git commit -am 'Add key'`
Run `git commit -am 'Add key' --no-verify`

### pre-commit specific hook

`export JIRA_USER=aandrieu`

`export JIRA_PASSWORD=XXX`

### The Templates Directories

# See [git-hooks-using-python](http://omerkatz.com/blog/2013/5/23/git-hooks-part-2-implementing-git-hooks-using-python)

## Local

First time run `cp hooks/* .git/hooks/` or `rm -Rf ./.git/hooks/ && ln -s ../hooks ./.git/hooks && git checkout hooks/`

## Global

We have two directories that interest us:

The '/usr/share/git-core/templates/' directory on Linux and 'C:/Program Files (x86)/Git/share/git-core/templates/' directory on Windows (Note that on 32bit machines msysGit is installed by default on 'C:/Program Files/…') in which the default hooks are being copied from. If you installed Git using another configuration the installation might reside in a different folder. Adjust the path accordingly.
The '.git/hooks/' directory is the directory in which the hooks templates are being copied to.
The hooked are being copied from the '[...]/share/git-core/templates/'  directory.  There are other types of templates but they are out of scope for this post.

Note:  If you change the templates directory the hooks directory  must be a subdirectory of the templates directory. Do not set the templates directory to the desired hooks directory instead.

Run `git config --global init.templatedir /workspace/users/albandri30/nabla-hooks/`
