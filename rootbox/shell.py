""" This module provides shell setup helper options with
extended capabilities for interactive shells """
import os
import shutil
from pathlib import Path

from .colorhelper import info
from .size import HumanSize


def raw_execute(image_name: str, moundir: Path, command: str) -> None:
    """Execute a command in the container without using a shell"""
    command = command.split()
    os.execvp(command[0], command[:])


def shell_execute(image_name: str, moundir: Path, command: str) -> None:
    """Execute the command in the container as a shell command
    or an interactive shell if no command is provided"""
    if command is None:
        command = "/bin/sh"
    is_interactive = command == "/bin/sh"
    if is_interactive:
        os.environ["PS1"] = f"\e[0;94m(rbox {image_name} \w)$ \e[m"
        print_system_info()
        os.execvp("/bin/sh", ["sh"])
    else:
        os.execvp("/bin/sh", ["sh", "-c", command])


def print_system_info():
    """Print system information"""
    cpu_count = len(os.sched_getaffinity(0))
    mem_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf(
        "SC_PHYS_PAGES"
    )  # e.g. 4015976448
    mem_size = info("{0:.2S}".format(HumanSize(mem_bytes)))
    print(
        f"* Running on host with {info(cpu_count)} CPU cores, {mem_size} RAM",
    )

    disk_usage = shutil.disk_usage("/")
    total = info("{0:.2S}".format(HumanSize(disk_usage.total)))
    used = info("{0:.2S}".format(HumanSize(disk_usage.used)))
    free = info("{0:.2S}".format(HumanSize(disk_usage.free)))
    print(
        f"* Rootbox in-memory mounted filesytem with {total} total, {used} used and {free} free."
    )
