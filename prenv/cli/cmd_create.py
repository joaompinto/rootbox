"""  Create a new environment  """
import os
import sys

import typer

from ..download import download
from ..lxc import LCXMetaData
from ..process import create_child_process


def check_distro_name(distro_name: str):
    return distro_name


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
    command: str = typer.Option("/bin/sh", "--command", "-c", help="Command to run"),
    until_tar: bool = typer.Option(
        False, "--until-tar", help="Pause with sh after extracting tar file"
    ),
):
    distro_url = get_distro_url(distro_name)
    typer.echo(f"Downloading file {distro_url} for {distro_name}")
    tar_fname = download(distro_url)
    pid = create_child_process(tar_fname)
    args = [sys.executable, "-m", "prenv", "join", str(pid), "--command", command]
    os.execvp(sys.executable, args)
