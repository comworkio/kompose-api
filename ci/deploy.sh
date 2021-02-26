#!/bin/bash

REPO_PATH="/home/centos/kompose-api/"

cd "${REPO_PATH}" && git pull origin main || :
docker rm -rf kompose-api_cmd-api_1 || :
docker-compose -f docker-compose-comwork.yml up -d
