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
    chroot_break: bool = typer.Option(False, "--break", help="Break into shell"),
):
    image = parse_image_url(image_name)
    image_fname = download_image(image)
    prepare_rootfs(image_fname, in_memory=True, perform_chroot=True)
    if no_shell:
        command = command.split()
        os.execvp(command[0], command[:])
    else:
        os.execvp("/bin/sh", ["sh", "-c", command])
