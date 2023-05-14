from pathlib import Path
from typing import Union

import typer

from .http import HTTPHandler
from .lxc import LXCHandler, validate_image_name

supported_handlers = ["lxc", "https", "http"]


def local_url(path: str) -> Path:
    return Path(path)


def parse_image_url(image_url: str) -> Union[LXCHandler, Path]:
    """Validate the image url and return the url parts
    An image_url containing an ':' is considered a remote image.
    The following remote handlers are supported: lxc, http, https
    A local image is a path to a file or directory

    Examples:
        lxc:disro:version[:variant]
        http://example.com/path/to/file.tar.gz
        https://example.com/path/to/file.tar.gz
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
            return LXCHandler(*url.split(":"))
        except TypeError:  # missing arguments
            validate_image_name(url)

    if handler in ["http", "https"]:
        return HTTPHandler(image_url)

    raise typer.BadParameter(
        f"Unknown image handler '{handler}',  Supported handlers: {supported_handlers}"
    )
