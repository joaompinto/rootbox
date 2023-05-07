import os
from pathlib import Path
from tempfile import mkdtemp

from .mount import MS_BIND, MS_PRIVATE, MS_REC, mount

STD_MOUNTS = [
    ("/", "host_root/", None, MS_BIND | MS_REC),
    ("/proc", "proc/", None, MS_BIND | MS_REC),
    ("/dev", "dev/", None, MS_BIND | MS_REC),
    ("/sys", "sys/", None, MS_BIND | MS_REC),
    ("tmpfs", "run/", "tmpfs"),
]


def create_root_tmpfs(ram_disk_size: int = 1):
    """Create a tmpfs file system and mount it on a random tmp directory"""
    if os.getuid() != 0:
        raise PermissionError("This function must be run with uid 0")
    mount(None, "/", None, MS_REC | MS_PRIVATE)
    mount_dir = Path(mkdtemp())
    mount("tmpfs", mount_dir, "tmpfs", options=f"size={ram_disk_size}G")
    return mount_dir


def bind_standard_mounts(mount_dir):
    """Create the standards mounts on top of mount_dir"""

    if os.getuid() != 0:
        raise PermissionError("This function must be run with uid 0")

    for mount_args in STD_MOUNTS:
        tmp_mount_args = list(mount_args)
        tmp_mount_args[1] = f"{mount_dir}/{tmp_mount_args[1]}"
        os.makedirs(tmp_mount_args[1])
        mount(*tmp_mount_args)


def bind_mount_to_host(mount_dir, path):
    target_path = Path(f"{mount_dir}{path}")

    if target_path.is_symlink():
        target_path.unlink()
    if target_path.parent.exists():
        target_path.touch()
        mount(path, target_path, None, MS_BIND)


def bind_working_dir(mount_dir):
    working_dir = os.getcwd()
    target_restore_path = Path(mount_dir, working_dir[1:])
    target_restore_path.mkdir(parents=True)
    mount(working_dir, target_restore_path, None, MS_BIND | MS_REC)
