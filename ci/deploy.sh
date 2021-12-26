#!/usr/bin/env bash

docker rmi -f "comworkio/kompose-api:latest" || :
docker-compose -f docker-compose-comwork.yml up -d --force-recreate
