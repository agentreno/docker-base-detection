# dockerinspect

## Description

Guide and helper scripts for Docker image manipulation. For example, this
started off as an exercise in finding out if one Docker image is based on
another and turned into a general utility library.

To simplify matters, a local registry is used which doesn't require
authentication.

## Install

Clone the repo and do `pip3 install .`

## Tutorial: Finding out if one docker image is based on another

### Setting up a registry and pushing images

- `docker run -d --name registry -p 5000:5000 registry`
- `docker tag ubuntu:latest localhost:5000/ubuntu:latest`
- `docker push localhost:5000/ubuntu:latest`

### Building an image based on ubuntu

- `docker build -t localhost:5000/base-detection-example:latest .`
- `docker push localhost:5000/base-detection-example:latest`

### Getting image manifests

- `http http://localhost:5000/v2/ubuntu/manifests/latest 'Accept:application/vnd.docker.distribution.manifest.v2+json'`
- `http http://localhost:5000/v2/base-detection-example/manifests/latest 'Accept:application/vnd.docker.distribution.manifest.v2+json'`

### Check image basis

```
import dockerinspect

registry_base = 'http://localhost:5000/'

client = dockerinspect.RegistryClient(registry_base)
base_image = client.get_image('ubuntu', 'latest')
child_image = client.get_image('base-detection-example', 'latest')

print(base_image.is_base_of(child_image))
```

## TODO

- Work out how to calculate digests
- Where are the signatures??
- Pull a layer and unzip it to inspect the diff
