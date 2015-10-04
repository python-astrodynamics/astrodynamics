#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew install findutils
    if [ -d "$HOME/Library/Caches/pip" ]; then
        gfind $HOME/Library/Caches/pip -type f -name '*.whl'  
    fi
else
    if [ -d "$HOME/.cache/pip" ]; then
        find $HOME/.cache/pip -type f -name '*.whl'  
    fi
fi
