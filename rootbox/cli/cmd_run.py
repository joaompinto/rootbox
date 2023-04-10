"""  Create a new environment  """
import os
from typing import Optional

import typer

from ..docker import pull_docker_image
from ..download import download
from ..rootfs import prepare_rootfs
from ..verbose import verbose
from .cmd_create import get_distro_url


def run(
    distro_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh"),
    from_docker: bool = typer.Option(
        False, "--from-docker", help="Run from docker image"
    ),
    command: Optional[str] = typer.Argument("/bin/sh", help="Command to be run"),
    chroot_break: bool = typer.Option(False, "--break", help="Break into shell"),
):
    if from_docker:
        tar_fname = pull_docker_image(distro_name)
    else:
        distro_url = get_distro_url(distro_name)
        verbose(f"Checking file {distro_url} for {distro_name}")
        tar_fname = download(distro_url)

    mount_dir = prepare_rootfs(tar_fname, in_memory=True)
    if chroot_break:
        os.chdir(mount_dir)
        os.system("bash")
        exit(0)
    os.chroot(mount_dir)
    os.chdir("/")
    if no_shell:
        command = command.split()
        os.execvp(command[0], command[:])
    else:
        os.execvp("/bin/sh", ["sh", "-c", command])
