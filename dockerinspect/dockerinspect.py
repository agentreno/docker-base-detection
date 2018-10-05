import re
import requests


class RegistryClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_image(self, name, tag='latest'):
        manifest = self.get_image_v2_manifest(name, tag)
        layers = []
        if 'layers' in manifest:
            layers = [layer['digest'] for layer in manifest['layers']]

        return DockerImage(name, tag, manifest, layers)

    def get_image_v2_manifest(self, name, tag):
        headers = {
            'Accept': 'application/vnd.docker.distribution.manifest.v2+json'
        }

        manifest_url = self.base_url + 'v2/{}/manifests/{}'
        manifest = None
        try:
            response = requests.get(
                manifest_url.format(name, tag),
                headers=headers
            )
            response.raise_for_status()
            manifest = response.json()
        except requests.exceptions.HTTPError as err:
            if err.response.status_code != 401:
                raise

            # Handle 401 Unauthorized by using Www-Authenticate header to get a
            # token from the auth service and retry
            match = re.search(
                'realm="(.+)",service="(.+)",scope="(.+)"',
                err.response.headers['Www-Authenticate']
            )
            if not match:
                raise

            realm, service, scope = match.groups()
            token = self.get_registry_token(realm, service, scope)
            headers['Authorization'] = 'Bearer ' + token
            response = requests.get(
                manifest_url.format(name, tag),
                headers=headers
            )
            response.raise_for_status()
            manifest = response.json()

        return manifest

    def get_registry_token(self, auth_url_base, service, scope):
        response = requests.get(
            auth_url_base + '?scope={}&service={}'.format(scope, service)
        )
        response.raise_for_status()

        return response.json()['token']


class DockerImage:
    def __init__(self, name, tag, manifest, layers):
        self.name = name
        self.tag = tag
        self.manifest = manifest
        self.layers = layers

    def is_base_of(self, image):
        for i, _ in enumerate(self.layers):
            if self.layers[i] != image.layers[i]:
                return False

        return True


if __name__ == '__main__':
    registry_base = 'http://localhost:5000/'

    client = RegistryClient(registry_base)
    base_image = client.get_image('ubuntu', 'latest')
    child_image = client.get_image('base-detection-example', 'latest')

    print(base_image.is_base_of(child_image))
