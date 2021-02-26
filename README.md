# Kompose API

An http api that aims to convert yaml from docker-compose into K8S manifests.

## Table of content

[[_TOC_]]

## Git repo

* Main repo: https://gitlab.comwork.io/oss/kompose-api
* Github mirror backup: https://github.com/idrissneumann/kompose-api
* Gitlab mirror backup: https://gitlab.com/ineumann/kompose-api

## Getting started

### Run the api using docker-compose

```shell
$ git clone https://gitlab.comwork.io/oss/kompose-api.git
$ cd kompose-api
$ docker-compose up -d
```

### Endpoints
#### Health check

```shell
$ curl http://0.0.0.0:8080/|jq .
{
  "status": "ok",
  "alive": true
}
```

#### Getting the kompose versions

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

The you'll have to refer to [kompose website](./https://kompose.io/) in order to get more informations such as compatibility matrix with docker-compose and kubernetes, etc.

### Manifest endpoint

```shell
$ curl http://0.0.0.0:8080/manifest|jq .
{
  "sha": "043633e19674a7b18a17cde26143ad94effe3dbd"
}
```

Get the last git sha used to build the image.