"""  Create a new environment  """
import os
from typing import Optional

import typer

from ..download import download_image
from ..images import parse_image_url
from ..rootfs import prepare_rootfs


def run(
    image_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh"),
    command: Optional[str] = typer.Argument("/bin/sh", help="Command to be run"),
    only_from_cache: bool = typer.Option(False, "--only-from-cache"),
):
    image = parse_image_url(image_name)
    image_fname = download_image(image, only_from_cache=only_from_cache)
    prepare_rootfs(image_fname, in_memory=True, perform_chroot=True)
    if no_shell:
        command = command.split()
        os.execvp(command[0], command[:])
    else:
        os.execvp("/bin/sh", ["sh", "-c", command])
