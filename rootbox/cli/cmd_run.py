"""  Create a new environment  """
import os
import tarfile
from pathlib import Path
from typing import Optional

import typer

from ..download import download_image
from ..images import parse_image_url
from ..rootfs import prepare_rootfs
from ..shell.execute import execute
from ..unshare import CLONE_NEWNET, unshare

MOUNT_DIR: Path = None


def run(
    image_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh", "--no-shell"),
    no_net: bool = typer.Option(
        False, "--no-network", "-N", help="Disable network in the container"
    ),
    command: Optional[str] = typer.Argument(None, help="Command to be run"),
    only_from_cache: bool = typer.Option(False, "--only-from-cache"),
    tar_file: Optional[Path] = typer.Option(None, "--tar-file", "-t"),
):
    global MOUNT_DIR
    if no_shell and command == "/bin/sh":
        raise typer.BadParameter("--no-shell was provided but no command was given")

    image = parse_image_url(image_name)
    if isinstance(image, Path):
        image_fname = image
    else:
        image_fname = download_image(image, only_from_cache=only_from_cache)
    mount_dir = prepare_rootfs(image_fname, in_memory=True, perform_chroot=True)
    if no_net:
        unshare(CLONE_NEWNET)
    execute(image_name, mount_dir, command, use_shell=not no_shell)
    # tar_file = Path("/hostroot") / tar_file.relative_to("/")
    os.chroot("/host_root")
    if tar_file:
        MOUNT_DIR = mount_dir
        with tarfile.open(tar_file, "w:gz") as tar:
            tar.add(
                mount_dir, arcname="./", filter=filter_out_other_mounts, recursive=True
            )


def filter_out_other_mounts(tarinfo: tarfile.TarInfo):
    global MOUNT_DIR
    filename = MOUNT_DIR.joinpath(tarinfo.name)
    if is_on_another_filesystem(filename):
        return None
    return tarinfo


def is_on_another_filesystem(path: Path):
    global MOUNT_DIR
    if path.is_symlink():
        return False
    if path == MOUNT_DIR:
        return False
    st = os.stat(path)
    current_dev = st.st_dev
    st = os.stat(path.parent)
    if st.st_dev != current_dev:
        return True
    return False
