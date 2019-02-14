Quality & Testing
=================

Commit Hook
-----------

Can be run using ``pre-commit`` tool (http://pre-commit.com/)::

   pre-commit install

First time run `cp hooks/* .git/hooks/` or `rm -Rf ./.git/hooks/ && ln -s ../hooks ./.git/hooks && git checkout hooks/`

   pre-commit run --all-files

   SKIP=flake8 git commit -am 'Add key'
   git commit -am 'Add key' --no-verify
