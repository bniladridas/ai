#!/bin/bash

# Script to rewrite commit messages
# Makes first line lowercase, truncates to 30 characters, removes types

git filter-branch --env-filter '
    export GIT_AUTHOR_NAME="Niladri Das"
    export GIT_AUTHOR_EMAIL="125604915+bniladridas@users.noreply.github.com"
    export GIT_COMMITTER_NAME="Niladri Das"
    export GIT_COMMITTER_EMAIL="125604915+bniladridas@users.noreply.github.com"
' --msg-filter '
    read msg
    first_line=$(echo "$msg" | head -n1)
    # Remove PR numbers like (#22)
    first_line=$(echo "$first_line" | sed "s/ (#.*)//")
    # Make lowercase
    first_line=$(echo "$first_line" | tr "[:upper:]" "[:lower:]")
    # Truncate to 30 chars
    first_line=$(echo "$first_line" | cut -c1-30)
    # Remove conventional type if present
    first_line=$(echo "$first_line" | sed 's/^[a-z]*: //')
    # Keep only first word
    first_line=$(echo "$first_line" | awk '{print $1}')
    # Reconstruct message
    rest=$(echo "$msg" | tail -n +2)
    echo "$first_line"
    if [ -n "$rest" ]; then
        echo "$rest"
    fi
' -- --all