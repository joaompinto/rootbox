from pathlib import Path
from typing import Union

import typer

from .lxc import LXCImage


def local_url(path: str) -> Path:
    return Path(path)


def parse_image_url(image_url: str) -> Union[LXCImage, Path]:
    """Validate the image url and return the url parts
    An image_url containing an ':' is considered a remote image.
    The following remote handlers are supported: lxc, http, https
    A local image is a path to a file or directory

    Examples:
        lxc:disro:version[:variant]
        /path/to/file.tar.gz
        /path/to/directory
    """
    if ":" not in image_url:
        return local_url(image_url)

    handler, url = image_url.split(":", 1)

    if url == "":
        raise typer.BadParameter(f" Got handler name'{handler}' with an empty url.")

    if handler == "lxc":
        try:
            return LXCImage(*url.split(":"))
        except TypeError:  # missing arguments
            return LXCImage.validate(url)

    raise typer.BadParameter(
        f"Unknown image handler '{handler}',  Supported handlers: 'lxc:'"
    )
