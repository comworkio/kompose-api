#!/bin/bash

cd /
v=$(env | grep "${1}" | cut -d "=" -f2 | sort -u)
jq -nc '$ARGS.positional' --args ${v[@]}
