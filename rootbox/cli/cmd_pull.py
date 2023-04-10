"""  pull an image from a remote repository  """
from pathlib import Path

import typer

from ..download import download_image
from ..images import parse_image_url


def pull(
    image_name: str = typer.Argument(...),
    ignore_cache: bool = typer.Option(
        False, "--ignore-cache", help="Ignore cached images"
    ),
):
    image = parse_image_url(image_name)
    if isinstance(image, Path):
        raise typer.BadParameter(
            "Only remote images are supported, name starting with  docker:, lxc:, http:, https:"
        )
    download_image(image, ignore_cache)
