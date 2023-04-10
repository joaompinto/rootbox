import hashlib
from os.path import basename
from tempfile import NamedTemporaryFile

import requests
from rich.progress import Progress

from rootbox.size import HumanSize

from .colorhelper import print_error, print_info


def download_url(image_url):
    """Download image (if not found in cache) and return it's filename"""

    response = requests.head(image_url, allow_redirects=True)
    response.raise_for_status()
    file_size = remote_file_size = int(response.headers.get("Content-Length"))
    remote_is_valid = response.status_code == 200 and file_size
    # Not cached, and no valid remote information was found
    if not remote_is_valid:
        print_error(
            "Unable to get file, http_code=%s, size=%s"
            % (
                response.status_code,
                remote_file_size,
            )
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
    return tmp_file.name
