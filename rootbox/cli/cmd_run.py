"""  Create a new environment  """
from typing import Optional

import typer

from ..download import download_image
from ..images import parse_image_url
from ..rootfs import prepare_rootfs
from ..shell import raw_execute, shell_execute
from ..unshare import CLONE_NEWNET, unshare


def run(
    image_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh", "--no-shell"),
    no_net: bool = typer.Option(
        False, "--no-network", "-N", help="Disable network in the container"
    ),
    command: Optional[str] = typer.Argument(None, help="Command to be run"),
    only_from_cache: bool = typer.Option(False, "--only-from-cache"),
):
    if no_shell and command == "/bin/sh":
        raise typer.BadParameter("--no-shell was provided but no command was given")

    image = parse_image_url(image_name)
    image_fname = download_image(image, only_from_cache=only_from_cache)
    mount_dir = prepare_rootfs(image_fname, in_memory=True, perform_chroot=True)
    if no_net:
        unshare(CLONE_NEWNET)
    if no_shell:
        raw_execute(image_name, mount_dir, command)
    else:
        shell_execute(image_name, mount_dir, command)
