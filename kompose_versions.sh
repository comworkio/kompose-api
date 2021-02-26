#!/bin/bash

cd /
v=$(env | grep KOMPOSE_VERSION | cut -d "=" -f2 | sort -u)
jq -nc '$ARGS.positional' --args ${v[@]}
