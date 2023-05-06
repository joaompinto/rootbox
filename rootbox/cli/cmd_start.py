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
    command: Optional[str] = typer.Argument(None, help="Command to be run"),
):
    pid = create_manager_process(image_name)
    config_dir = Path.home().joinpath(".rootbox")
    config_dir.mkdir(exist_ok=True)
    Path(config_dir, ".lastpid").write_text(str(pid))
    if command:
        args = [sys.executable, "-m", "rootbox", "join", str(pid), command]
        # Respect the no-sh behavior
        if no_shell:
            args.insert(4, "--no-sh")
        os.execvp(sys.executable, args)
