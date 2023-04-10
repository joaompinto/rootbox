"""  Create a new environment  """
import os
import sys
from typing import Optional

import typer

from ..docker import pull_docker_image
from ..download import download
from ..lxc import LCXMetaData
from ..process import create_child_process
from ..verbose import verbose


def get_distro_url(distro_name: str):
    lcx = LCXMetaData()
    distro_version = None
    if ":" in distro_name:
        distro_name, distro_version = distro_name.split(":")
    if distro_name not in lcx.distros():
        raise typer.BadParameter(f"Unknown distro {distro_name}")
    return lcx.image_url(distro_name, distro_version=distro_version)


def create(
    distro_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh"),
    from_docker: bool = typer.Option(
        False, "--from-docker", help="Run from docker image"
    ),
    command: Optional[str] = typer.Argument(None, help="Command to be run"),
):
    if from_docker:
        tar_fname = pull_docker_image(distro_name)
    else:
        distro_url = get_distro_url(distro_name)
        verbose(f"Checking file {distro_url} for {distro_name}")
        tar_fname = download(distro_url)
    pid = create_child_process(tar_fname)
    if command:
        args = [sys.executable, "-m", "rootbox", "join", str(pid), command]
        # Respect the no-sh behavior
        if no_shell:
            args.insert(4, "--no-sh")
        os.execvp(sys.executable, args)
