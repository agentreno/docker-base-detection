# docker-base-detection

## Description

Guide and helper scripts to find out if one Docker image is based on another.
To simplify matters, a local registry is used which doesn't require
authentication.

## Setting up a registry and pushing images

- `docker run -d --name registry -p 5000:5000 registry`
- `docker tag ubuntu:latest localhost:5000/ubuntu:latest`
- `docker push localhost:5000/ubuntu:latest`

## Building an image based on ubuntu

- `docker build -t localhost:5000/base-detection-example:latest .`
- `docker push localhost:5000/base-detection-example:latest`

## Getting image manifests

- `http http://localhost:5000/v2/ubuntu/manifests/latest 'Accept:application/vnd.docker.distribution.manifest.v2+json'`
- `http http://localhost:5000/v2/base-detection-example/manifests/latest 'Accept:application/vnd.docker.distribution.manifest.v2+json'`

## TODO

- Work out how to calculate digests
- Where are the signatures??
- Pull a layer and unzip it to inspect the diff
- Write code to detect base image
