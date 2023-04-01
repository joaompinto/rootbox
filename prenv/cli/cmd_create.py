"""  Create a new environment  """
import os

import typer

from ..download import download
from ..lxc import LCXMetaData
from ..rootfs import prepare_rootfs


def check_distro_name(distro_name: str):
    return distro_name


def create(
    distro_name: str = typer.Argument(...),
    until_tar: bool = typer.Option(
        False, "--until-tar", help="Pause with sh after extracting tar file"
    ),
):
    lcx = LCXMetaData()
    distro_version = None
    if ":" in distro_name:
        distro_name, distro_version = distro_name.split(":")
    if distro_name not in lcx.distros():
        raise typer.BadParameter(f"Unknown distro {distro_name}")
    distro_url = lcx.image_url(distro_name, distro_version=distro_version)

    typer.echo(f"Downloading file {distro_url} for {distro_name}")
    tar_fname = download(distro_url)
    print("Extracting rootfs... ", end="", flush=True)
    prepare_rootfs(tar_fname, until_tar)
    print("\nChrooting into rootfs")
    os.chroot(".")
    os.execv("/bin/sh", ["/bin/sh"])
