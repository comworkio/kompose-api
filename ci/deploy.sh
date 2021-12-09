#!/bin/bash

REPO_PATH="${PROJECT_HOME}/kompose-api/"

cd "${REPO_PATH}" && git pull origin main || :
docker rm -f kompose-api_kompose-api_1 || :
docker-compose -f docker-compose-comwork.yml up -d
