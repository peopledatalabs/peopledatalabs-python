#! /bin/bash

set -e

FILES_TO_LINT=$(git ls-files "*.py")

pylint $FILES_TO_LINT
flake8 $FILES_TO_LINT
docformatter -c $FILES_TO_LINT \
        --pre-summary-newline \
        --make-summary-multi-line
black . --check --diff
autoflake -c $FILES_TO_LINT \
        --remove-duplicate-keys \
        --remove-unused-variables \
        --remove-all-unused-imports

echo
echo "-------------------------------------------"
echo
echo "Looking neat! 👌"
