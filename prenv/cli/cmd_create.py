import os

import typer

from ..distros import URL_MAP
from ..download import download
from ..rootfs import prepare_rootfs


def check_distro_name(distro_name: str):
    return distro_name


def create(
    distro_name: str = typer.Argument(...),
    until_tar: bool = typer.Option(
        False, "--until-tar", help="Pause with sh after extracting tar file"
    ),
):
    distro_url = URL_MAP.get(distro_name)
    if not distro_url:
        raise typer.BadParameter(f"Unknown distro {distro_name}")

    typer.echo(f"Downloading file {distro_url} for {distro_name}")
    tar_fname = download(distro_url)
    print("Extracting rootfs... ", end="", flush=True)
    prepare_rootfs(tar_fname, until_tar)
    print("\nChrooting into rootfs")
    os.chroot(".")
    os.execv("/bin/sh", ["/bin/sh"])
