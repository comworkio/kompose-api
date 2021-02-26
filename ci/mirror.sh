#!/bin/bash

REPO_PATH="/home/centos/kompose-api/"

cd "${REPO_PATH}" && git pull origin main || :
git push github main 
git push pgitlab main
exit 0
