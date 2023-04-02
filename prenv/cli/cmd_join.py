"""  Create a new environment  """

import typer

from ..enter import enter_process


def join(
    pid: int,
    command: str = typer.Option("/bin/sh", "--command", "-c", help="Command to run"),
):
    enter_process(pid, command.split(" "))
