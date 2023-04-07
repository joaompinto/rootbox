from tempfile import NamedTemporaryFile

from drclient.cli.cmd_pull import pull
from drclient.registry import DockerRegistryClient

from .download import Cache


def pull_docker_image(image_name):
    registry, repository, tag = DockerRegistryClient.parse_image_url(image_name)
    source_reference = f"{registry}/{repository}:{tag}"
    return download(source_reference)


def download(image_url, use_cache=True):
    # Check if image is on cache
    if use_cache:
        cache = Cache()
        cached_image = cache.get(image_url)
        if cached_image:
            cache_fn, last_modified, file_size = cached_image
            return cache_fn
    with NamedTemporaryFile(delete=False) as tmp_file:
        pull(image_url, tar_file=tmp_file.name, output_directory=None)
        tmp_file.flush()
    if use_cache:
        return cache.put(tmp_file.name, image_url)
    return tmp_file.name
