import os
import shutil

from ..colorhelper import info
from ..size import HumanSize


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
