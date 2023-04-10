import hashlib
import os
import shutil
from datetime import datetime
from os.path import basename, exists, expanduser, join
from tempfile import NamedTemporaryFile

import requests
from dateutil.parser import parse as parsedate
from rich.progress import Progress

from .colorhelper import print_error, print_info, print_warn
from .size import HumanSize
from .verbose import verbose

CACHE_PATH = join(expanduser("~"), ".rootbox", "images_cache")


def url_to_filename(url: str):
    """Convert url to filename"""
    url = url.replace("://", "_")
    url = url.replace("/", "_")
    url = url.replace(":", "_")
    return url


class Cache(object):
    cache_dir = CACHE_PATH
    """ Provides an image caching mechanism on disk """

    def __init__(self):
        if not exists(CACHE_PATH):
            os.makedirs(CACHE_PATH, 0o700)

    def get(self, cache_key, default=None):
        """return info for cached file"""

        cache_fn = join(CACHE_PATH, url_to_filename(cache_key))

        if exists(cache_fn):
            file_stat = os.stat(cache_fn)
            last_modified = datetime.fromtimestamp(file_stat.st_mtime)
            file_size = file_stat.st_size
            return cache_fn, last_modified, file_size

        return default

    def put(self, filename, cache_key):
        """put a file into cache"""
        cache_fn = join(CACHE_PATH, url_to_filename(cache_key))
        shutil.move(filename, cache_fn)
        return cache_fn


def download(image_url, use_cache=True):
    """Download image (if not found in cache) and return it's filename"""

    response = requests.head(image_url, allow_redirects=True)
    response.raise_for_status()
    file_size = remote_file_size = int(response.headers.get("Content-Length"))
    remote_last_modified = parsedate(response.headers.get("Last-Modified")).replace(
        tzinfo=None
    )
    remote_is_valid = response.status_code == 200 and file_size and remote_last_modified

    # Check if image is on cache
    if use_cache:
        cache = Cache()
        cached_image = cache.get(image_url)
    else:
        cached_image = None
    if cached_image:
        if remote_is_valid:
            cache_fn, last_modified, file_size = cached_image
            if remote_file_size == file_size and remote_last_modified < last_modified:
                verbose("Using file from cache", CACHE_PATH)
                return cache_fn
            verbose("Checking new remote file because an update was found")
        else:
            print_warn("Unable to check the status for " + image_url)
            print_warn("Assuming local cache is valid")

    # Not cached, and no valid remote information was found
    if not remote_is_valid:
        print_error(
            "Unable to get file, http_code=%s, size=%s, last_modified=%s"
            % (response.status_code, remote_file_size, remote_last_modified)
        )
        exit(2)

    # Dowload image
    print_info(
        "Downloading image... ",
        "{0} [{1:.2S}]".format(basename(image_url), HumanSize(remote_file_size)),
    )
    remote_sha256 = hashlib.sha256()
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    with NamedTemporaryFile(delete=False) as tmp_file:
        with Progress() as progress:
            task1 = progress.add_task("[green]Processing...", total=remote_file_size)
            for chunk in response.iter_content(chunk_size=1024):
                remote_sha256.update(chunk)
                tmp_file.write(chunk)
                progress.update(task1, advance=len(chunk))
            tmp_file.flush()
    if use_cache:
        return cache.put(tmp_file.name, image_url)
    else:
        return tmp_file.name
