# Kompose API

An http api that aims to convert yaml from docker-compose into K8S manifests.

An instance of this API is available here: https://kompose.comwork.io

It's based on kompose.io and available as a "Kompose as a service".

Basically you can directly deploy your docker-compose file using one single command:

```shell
curl -X POST https://kompose.comwork.io/ -F "file=@docker-compose.yml" | kubectl -n your-namespace apply -f -
```

or

```shell
curl -X POST https://kompose.k8s.yourcluster.io/ -F "file=@docker-compose.yml" -H "X-K8S-Apply: true" -H "X-K8S-NS: your-namespace"
```

In the case where you've deployed your own instance on your own cluster with the right service-account (of course you'll have to replace `https://kompose.k8s.yourcluster.io` by your own url).

## Table of content

[[_TOC_]]

## Git repo

* Main repo: https://gitlab.comwork.io/oss/kompose-api
* Github mirror backup: https://github.com/idrissneumann/kompose-api
* Gitlab mirror backup: https://gitlab.com/ineumann/kompose-api
* Bitbucket mirror backup: https://bitbucket.org/idrissneumann/kompose-api

## Docker hub repo

The image is available here: https://hub.docker.com/repository/docker/comworkio/kompose-api

You can run it wherever there is an OCI runtime container available (docker, kubernetes, podman, etc).

## Getting started

### Run the api using docker-compose

```shell
$ git clone https://gitlab.comwork.io/oss/kompose-api.git
$ cd kompose-api
$ docker-compose up -d
```

Then, you'll be able to use the available endpoints below using `http://0.0.0.0:8080/` instead of `https://kompose.comwork.io`.

### Endpoints

#### Health check

```shell
$ curl https://kompose.comwork.io|jq .
{
  "status": "ok",
  "alive": true
}
```

#### Getting the kompose versions

```shell
curl https://kompose.comwork.io/versions|jq .
{
  "status": "ok",
  "kompose_versions": [
    "1.21.0",
    "1.22.0"
  ],
  "kubectl_versions": [
    "1.18.2"
  ]
}
```

The you'll have to refer to [kompose website](https://kompose.io/) in order to get more informations such as compatibility matrix with docker-compose and kubernetes, etc.

#### Getting an html rendered documentation

Follow this link: https://kompose.comwork.io/doc

#### Convert a docker-compose file into Kubernetes manifest

```shell
$ curl -X POST https://kompose.comwork.io/ -F "file=@docker-compose.yml"
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
* `X-K8S-NS`: specify the kubernetes namespace
* `X-K8S-Apply`: directly apply on the cluster (enabled if the environment variable `ENABLE_KUBECTL_APPLY` is set with `true`)

#### Manifest endpoint

```shell
$ curl "https://kompose.comwork.io/manifest"|jq .
{
  "version": "1.0",
  "sha": "ec4015c",
  "arch": "x86"
}
```

Get the last git sha used to build the image.
