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
def info(item: str):
    print(f"info item: {item}")
