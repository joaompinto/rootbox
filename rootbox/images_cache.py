import shutil
from pathlib import Path

CACHE_PATH: Path = Path.home() / ".rootbox" / "images_cache"


class Cache(object):
    cache_dir = CACHE_PATH
    """ Provides an image caching mechanism on disk """

    def __init__(self):
        CACHE_PATH.mkdir(parents=True, exist_ok=True)

    def get(self, cache_key, default=None):
        """return info for cached file"""
        cached_fname = CACHE_PATH.joinpath(cache_key)

        if cached_fname.exists():
            return cached_fname

        return default

    def get_all(self, cache_key, default=None):
        for extension in [".tar.gz"]:
            find = self.get(cache_key + extension)
            if find:
                return find
        return default

    def put(self, filename, cache_key):
        """put a file into cache"""
        cached_fname = CACHE_PATH.joinpath(cache_key)
        if ".tar" not in cached_fname.suffixes:
            cached_fname = Path(f"{cached_fname}.tar.gz")
        shutil.move(filename, cached_fname)
        return cached_fname
