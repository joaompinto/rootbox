"""  Create a new environment  """

from typing import Optional

import typer

from ..enter import enter_process


def exec(
    pid: int,
    no_shell: bool = typer.Option(False, "--no-sh"),
    command: Optional[str] = typer.Argument("/bin/sh", help="Command to be run"),
):
    enter_process(pid, no_shell, command)
