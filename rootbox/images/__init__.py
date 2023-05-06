from pathlib import Path
from typing import Union

import typer

from ..images_cache import Cache
from .lxc import LXCImage, validate_image_name


def local_url(path: str) -> Path:
    return Path(path)


cache = Cache()


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
            validate_image_name(url)

    raise typer.BadParameter(
        f"Unknown image handler '{handler}',  Supported handlers: 'lxc:'"
    )


def download_image(
    image: LXCImage, ignore_cache=False, only_from_cache=False, verbose_cache_info=False
):
    """Download image (if not found in cache) and return it's filename"""
    assert not (
        ignore_cache and only_from_cache
    )  # ignore_cache and only_from_cache are mutually exclusive

    cache_key = image.as_url()
    if ignore_cache:
        cached_fname = None
    else:
        cached_fname = cache.get_all(cache_key)

    if cached_fname:
        if verbose_cache_info:
            print(f"Found cached image at {cached_fname}")
        return cached_fname
    else:
        if only_from_cache:
            raise ValueError(f"Image {image.as_url()} not found in cache")

    fname = image.download()
    return cache.put(fname, cache_key)
