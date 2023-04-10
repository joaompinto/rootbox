"""  Create a new environment  """
import os
import sys
from typing import Optional

import typer

from ..download import download_image
from ..images import parse_image_url
from ..process import create_child_process


def create(
    image_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh", help="Run command without a shell"),
    command: Optional[str] = typer.Argument(None, help="Command to be run"),
):
    image = parse_image_url(image_name)
    image_fname = download_image(image)
    pid = create_child_process(image_fname)
    if command:
        args = [sys.executable, "-m", "rootbox", "join", str(pid), command]
        # Respect the no-sh behavior
        if no_shell:
            args.insert(4, "--no-sh")
        os.execvp(sys.executable, args)
