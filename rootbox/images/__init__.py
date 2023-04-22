from pathlib import Path
from typing import Union

import typer

from .docker import DockerImage
from .docker import parse_image_url as parse_docker_url
from .lxc import LXCImage


def local_url(path: str) -> Path:
    return Path(path)


def parse_image_url(image_url: str) -> Union[LXCImage, DockerImage, Path]:
    """Validate the image url and return the url parts
    An image_url containing an ':' is considered a remote image.
    The following remote handlers are supported: lxc, docker, http, https
    A local image is a path to a file or directory

    Examples:
        lxc:distro[:version][:variant]
        docker:image[:tag]
        docker:[repository/]image[:tag]
        https://url.tar.g
        /path/to/file.tar.gz
        /path/to/directory
    """
    if ":" not in image_url:
        return local_url(image_url)

    handler, url = image_url.split(":", 1)

    if handler == "lxc":
        return LXCImage(*url.split(":"))
    if handler == "docker":
        return DockerImage(*parse_docker_url(url))
    raise typer.BadParameter(
        f"Unknown image handler '{handler}', images must be prefixed with 'lxc:' or 'docker:"
    )
