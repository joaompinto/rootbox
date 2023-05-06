from .images import LXCImage
from .images_cache import Cache

cache = Cache()


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
