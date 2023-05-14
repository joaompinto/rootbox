"""  Create a new environment  """
import os
import tarfile
from pathlib import Path
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from rootbox.images import pull
from rootbox.images.tar import extract_tar

from ..rootfs import RootFS
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
    command: Annotated[str, typer.Argument(help="Command to be run")] = None,
    tar_file: Optional[Path] = typer.Option(None, "--tar-file", "-t"),
):
    if no_shell and command == "/bin/sh":
        raise typer.BadParameter("--no-shell was provided but no command was given")

    rootfs = RootFS(ram_disk_size)
    root_mnt = rootfs.get_root()

    if ":" in image_name:
        image_fname = pull(image_name)
    extract_tar(image_fname, root_mnt)

    rootfs.chroot()

    if no_net:
        unshare(CLONE_NEWNET)

    execute(image_name, command, use_shell=not no_shell)
    os.chroot("/host_root")
    if tar_file:
        print(f"Saving the container to {tar_file}", end="... ", flush=True)
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(root_mnt, arcname="./", recursive=True)
        print("Done")
