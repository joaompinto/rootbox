from .images import DockerImage, LXCImage
from .images_cache import Cache

cache = Cache()


def download_image(image: LXCImage | DockerImage, ignore_cache=False):
    """Download image (if not found in cache) and return it's filename"""

    cache_key = image.as_url()
    if ignore_cache:
        cached_fname = None
    else:
        cached_fname = cache.get(cache_key)

    if cached_fname:
        return cached_fname

    fname = image.download()
    return cache.put(fname, cache_key)
