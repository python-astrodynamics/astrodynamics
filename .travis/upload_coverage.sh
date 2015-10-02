#!/bin/bash

set -e
set -x

NO_COVERAGE_TOXENVS=(py32 py2flake8 py3flake8)
if ! [[ "${NO_COVERAGE_TOXENVS[*]}" =~ "${TOXENV}" ]]; then
    source ~/.venv/bin/activate
    wget https://codecov.io/bash -O codecov.sh
    bash codecov.sh -e TRAVIS_OS_NAME,TOXENV
fi
