FILES_TO_LINT=$(git ls-files "*.py")

pylint $FILES_TO_LINT
flake8 $FILES_TO_LINT
