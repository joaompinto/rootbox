"""  Create a new environment  """
import os
import tarfile
from pathlib import Path
from typing import Optional

import typer

from ..download import download_image
from ..images import parse_image_url
from ..mount_checker import MountChecker
from ..rootfs import prepare_rootfs
from ..shell.execute import execute
from ..unshare import CLONE_NEWNET, unshare


def run(
    image_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh", "--no-shell"),
    no_net: bool = typer.Option(
        False, "--no-network", "-N", help="Disable network in the container"
    ),
    ram_disk_size: Optional[int] = typer.Option(
        1, "--ram-disk", "-r", help="Size of the ram disk (GBs)"
    ),
    command: Optional[str] = typer.Argument(None, help="Command to be run"),
    only_from_cache: bool = typer.Option(False, "--only-from-cache"),
    tar_file: Optional[Path] = typer.Option(None, "--tar-file", "-t"),
):
    if no_shell and command == "/bin/sh":
        raise typer.BadParameter("--no-shell was provided but no command was given")

    image = parse_image_url(image_name)
    if isinstance(image, Path):
        image_fname = image
        image_prompt_name = f"file:{image.name}"
    else:
        image_fname = download_image(image, only_from_cache=only_from_cache)
        image_prompt_name = image_name
    mount_dir = prepare_rootfs(image_fname, ram_disk_size, perform_chroot=True)

    if no_net:
        unshare(CLONE_NEWNET)
    execute(image_prompt_name, mount_dir, command, use_shell=not no_shell)
    MountChecker.read_mounts()
    os.chroot("/host_root")
    if tar_file:
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(
                mount_dir, arcname="./", filter=filter_out_other_mounts, recursive=True
            )


def filter_out_other_mounts(tarinfo: tarfile.TarInfo):
    if MountChecker.is_on_mount_dir(tarinfo.name):
        return tarinfo
