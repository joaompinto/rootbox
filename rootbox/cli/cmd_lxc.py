""" Provide information about container images available from LXC """
from typing import Optional

import typer

from ..colorhelper import print_list
from ..images.lxc import LCXMetaData

app = typer.Typer()


@app.command()
def list(item: Optional[str] = typer.Argument(None)):
    lcx_meta = LCXMetaData()
    print_list("Distros", lcx_meta.distros())


@app.command()
def info(distro_name: str):
    lcx_meta = LCXMetaData()
    if distro_name not in lcx_meta.distros():
        error_text = (
            f"Unknown distro `{distro_name}`\n"
            f"Known distros: {', '.join(lcx_meta.distros())}"
        )
        raise typer.BadParameter(error_text)
    versions = ", ".join([version for version in lcx_meta.get_versions(distro_name)])
    print(f"Versions for `{distro_name} (amd64)`: {versions}")
