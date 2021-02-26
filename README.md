# Kompose API

An http api that aims to convert yaml from docker-compose into K8S manifests.

## Table of content

[[_TOC_]]

## Git repo

* Main repo: https://gitlab.comwork.io/oss/kompose-api
* Github mirror backup: https://github.com/idrissneumann/kompose-api
* Gitlab mirror backup: https://gitlab.com/ineumann/kompose-api

## Endpoints
### Health check

```shell
$ curl http://0.0.0.0:8080/|jq .
{
  "status": "ok",
  "alive": true
}
```

### Getting the compose versions

```shell
curl http://0.0.0.0:8080/kompose/versions|jq .
{
  "status": "ok",
  "available_pipelines": [
    "1.21.0",
    "1.22.0"
  ]
}
```