#!/bin/bash

REPO_PATH="/home/centos/kompose-api/"

cd "${REPO_PATH}" && git pull origin main || :
docker rm -f kompose-api_kompose-api_1 || :
docker-compose -f docker-compose-comwork.yml up -d
