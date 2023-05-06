"""  Create a new environment  """

from pathlib import Path

import typer
from typing_extensions import Annotated

from ..enter import enter_process


def exec(
    command: Annotated[str, typer.Argument(help="Command to be run")] = None,
    no_shell: bool = typer.Option(
        False,
        "--no-sh",
    ),
):
    config_dir = Path.home().joinpath(".rootbox")
    pid = int(Path(config_dir, ".lastpid").read_text())
    enter_process(pid, no_shell, command)
