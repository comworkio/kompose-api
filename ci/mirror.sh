#!/bin/bash

REPO_PATH="${PROJECT_HOME}/kompose-api/"

cd "${REPO_PATH}" && git pull origin main || :
git push github main 
git push pgitlab main
git push bitbucket main
git push froggit main
exit 0
