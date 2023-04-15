""" This module provides shell setup helper options with
extended capabilities for interactive shells """
import os
import subprocess
from pathlib import Path

from .systeminfo import print_system_info


def execute(
    image_name: str, moundir: Path, command: str, use_shell: bool = True
) -> None:
    """Execute the command in the container as a shell command
    or an interactive shell if no command is provided"""
    if command is None:
        command = "/bin/sh"
    is_interactive = command == "/bin/sh"
    if is_interactive:
        os.environ["PS1"] = f"\e[0;94m(rbox {image_name} \w)$ \e[m"
        print_system_info()
    if command == "/bin/sh":
        use_shell = False
    subprocess.call(command, shell=use_shell)
