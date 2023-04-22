from dataclasses import dataclass
from os import environ
from tempfile import NamedTemporaryFile

from drclient.image import parse_image_url as docker_parse_image_url
from drclient.image import pull_image

DEFAULT_REGISTRY = environ.get("DOCKER_REGISTRY", "registry-1.docker.io")


@dataclass
class DockerImage:
    registry: str
    image_name: str
    image_tag: str = "latest"

    def as_url(self) -> str:
        registry = self.registry.replace(".", "_")
        return url_to_filename(f"docker_{registry}_{self.image_name}_{self.image_tag}")

    def download(self):
        return pull_docker_image(self.registry, self.image_name, self.image_tag)


def pull_docker_image(registry, repository, tag):
    source_reference = f"{registry}/{repository}:{tag}"
    return download(source_reference)


def download(image_url):
    # Check if image is on cache
    with NamedTemporaryFile(delete=False) as tmp_file:
        pull_image(image_url, tar_file=tmp_file.name, output_directory=None)
        tmp_file.flush()
    return tmp_file.name


def parse_image_url(image_url: str) -> DockerImage:
    return docker_parse_image_url(image_url)


def url_to_filename(url: str):
    """Convert url to filename"""
    url = url.replace("://", "_")
    url = url.replace("/", "_")
    url = url.replace(":", "_")
    return url
