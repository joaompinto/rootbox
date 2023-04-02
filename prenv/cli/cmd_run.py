"""  Create a new environment  """
import os
from typing import Optional

import typer

from ..download import download
from ..rootfs import prepare_rootfs
from ..verbose import verbose
from .cmd_create import get_distro_url


def run(
    distro_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh"),
    command: Optional[str] = typer.Argument("/bin/sh", help="Command to be run"),
):
    distro_url = get_distro_url(distro_name)
    verbose(f"Checking file {distro_url} for {distro_name}")
    tar_fname = download(distro_url)
    mount_dir = prepare_rootfs(tar_fname, in_memory=True)
    os.chroot(mount_dir)
    os.chdir("/")
    if no_shell:
        command = command.split()
        os.execvp(command[0], command[:])
    else:
        os.execvp("/bin/sh", ["sh", "-c", command])
