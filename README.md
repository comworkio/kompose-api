# Kompose API

An http api that aims to convert yaml from docker-compose into K8S manifests.

An instance of this API is available here: https://kompose.comwork.io

## Table of content

[[_TOC_]]

## Git repo

* Main repo: https://gitlab.comwork.io/oss/kompose-api
* Github mirror backup: https://github.com/idrissneumann/kompose-api
* Gitlab mirror backup: https://gitlab.com/ineumann/kompose-api

## Getting started

### Hosted by comwork



### Run the api using docker-compose

```shell
$ git clone https://gitlab.comwork.io/oss/kompose-api.git
$ cd kompose-api
$ docker-compose up -d
```

### Endpoints

The following endpoints are also available here: https://kompose.comwork.io

So you can for each one replace `http://0.0.0.0:8080/` by `https://kompose.comwork.io`
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
curl http://0.0.0.0:8080/versions|jq .
{
  "status": "ok",
  "available_versions": [
    "1.21.0",
    "1.22.0"
  ]
}
```

The you'll have to refer to [kompose website](./https://kompose.io/) in order to get more informations such as compatibility matrix with docker-compose and kubernetes, etc.

### Convert a docker-compose file into Kubernetes manifest

```shell
$ curl -X POST http://0.0.0.0:8080/ -F "file=@docker-compose.yml"
apiVersion: v1
items:
  - apiVersion: v1
    kind: Service
    metadata:
      annotations:
        kompose.cmd: kompose-1.22.0 convert -f docker-compose-6754a9a0-782b-11eb-8358-0242ac1a0002.yml -o docker-compose-6754a9a0-782b-11eb-8358-0242ac1a0002.yml.k8s.yml
        kompose.version: 1.22.0 (955b78124)
      creationTimestamp: null
      labels:
        io.kompose.service: kompose-api
      name: kompose-api
    spec:
      ports:
        - name: "8080"
          port: 8080
          targetPort: 8080
      selector:
        io.kompose.service: kompose-api
    status:
      loadBalancer: {}
  - apiVersion: apps/v1
    kind: Deployment
    metadata:
      annotations:
        kompose.cmd: kompose-1.22.0 convert -f docker-compose-6754a9a0-782b-11eb-8358-0242ac1a0002.yml -o docker-compose-6754a9a0-782b-11eb-8358-0242ac1a0002.yml.k8s.yml
        kompose.version: 1.22.0 (955b78124)
      creationTimestamp: null
      labels:
        io.kompose.service: kompose-api
      name: kompose-api
    spec:
      replicas: 1
      selector:
        matchLabels:
          io.kompose.service: kompose-api
      strategy: {}
      template:
        metadata:
          annotations:
            kompose.cmd: kompose-1.22.0 convert -f docker-compose-6754a9a0-782b-11eb-8358-0242ac1a0002.yml -o docker-compose-6754a9a0-782b-11eb-8358-0242ac1a0002.yml.k8s.yml
            kompose.version: 1.22.0 (955b78124)
          creationTimestamp: null
          labels:
            io.kompose.service: kompose-api
        spec:
          containers:
            - image: comworkio/kompose-api:latest
              name: kompose-api
              ports:
                - containerPort: 8080
              resources: {}
          restartPolicy: Always
    status: {}
kind: List
metadata: {}
```

Note: the following headers are available:
* `X-Kompose-Version`: the version of `kompose` you want to use (see the previous endpoint to see which versions are avaible)
* `X-K8S-Provider`: the K8S provider (i.e: `OpenShift`)

### Manifest endpoint

```shell
$ curl http://0.0.0.0:8080/manifest|jq .
{
  "sha": "043633e19674a7b18a17cde26143ad94effe3dbd"
}
```

Get the last git sha used to build the image.