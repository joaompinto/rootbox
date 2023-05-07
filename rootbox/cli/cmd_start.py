"""  Create a new environment  """
import os
import sys
from pathlib import Path
from typing import Optional

import typer

from ..process import create_manager_process


def start(
    image_name: str = typer.Argument(...),
    no_shell: bool = typer.Option(False, "--no-sh", help="Run command without a shell"),
    ram_disk_size: Optional[int] = typer.Option(
        1, "--ram-disk", "-r", help="Size of the ram disk (GBs)"
    ),
    command: Optional[str] = typer.Argument(None, help="Command to be run"),
):
    pid = create_manager_process(image_name, ram_disk_size)
    config_dir = Path.home().joinpath(".rootbox")
    config_dir.mkdir(exist_ok=True)
    Path(config_dir, ".lastpid").write_text(str(pid))
    if command:
        args = [sys.executable, "-m", "rootbox", "join", str(pid), command]
        # Respect the no-sh behavior
        if no_shell:
            args.insert(4, "--no-sh")
        os.execvp(sys.executable, args)
