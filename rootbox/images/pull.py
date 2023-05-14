from .cache import Cache
from .url_parser import parse_image_url


def pull(image_url: str, verbose_cache_info: bool = False, ignore_cache: bool = False):
    """Download image (if not found in cache) and return it's filename"""
    cache = Cache()
    image = parse_image_url(image_url)
    cache_key = image.cache_key()
    if ignore_cache:
        cached_fname = None
    else:
        cached_fname = cache.get_all(cache_key)

    if cached_fname:
        if verbose_cache_info:
            print(f"Found cached image at {cached_fname}")
        return cached_fname
    fname = image.download()
    return cache.put(fname, cache_key)
