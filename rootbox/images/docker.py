from dataclasses import dataclass
from os import environ
from tempfile import NamedTemporaryFile

from drclient.cli.cmd_pull import pull

DEFAULT_REGISTRY = environ.get("DOCKER_REGISTRY", "registry-1.docker.io")


@dataclass
class DockerImage:
    registry: str
    image_name: str
    image_tag: str = "latest"

    def as_url(self) -> str:
        return url_to_filename(
            f"docker_{self.registry}_{self.image_name}_{self.image_tag}"
        )

    def download(self):
        return pull_docker_image(self.registry, self.image_name, self.image_tag)


def pull_docker_image(registry, repository, tag):
    source_reference = f"{registry}/{repository}:{tag}"
    return download(source_reference)


def download(image_url):
    # Check if image is on cache
    with NamedTemporaryFile(delete=False) as tmp_file:
        pull(image_url, tar_file=tmp_file.name, output_directory=None)
        tmp_file.flush()
    return tmp_file.name


def parse_docker_url(image_name: str) -> tuple:
    registry = DEFAULT_REGISTRY
    tag = "latest"
    if "/" in image_name:
        first_part, other_parts = image_name.split("/", 1)
        if "." in first_part:
            image_name = other_parts
            registry = f"{first_part}"
    else:
        image_name = f"library/{image_name}"
    if ":" in image_name:
        image_name, tag = image_name.split(":")
    return DockerImage(registry, image_name, tag)


def url_to_filename(url: str):
    """Convert url to filename"""
    url = url.replace("://", "_")
    url = url.replace("/", "_")
    url = url.replace(":", "_")
    return url
