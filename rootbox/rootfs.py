import os
from pathlib import Path
from tempfile import mkdtemp

from .mount import MS_BIND, MS_PRIVATE, MS_REC, mount
from .path import path_is_parent
from .unshare import setup_user_level_root

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
        target_mount_dir = f"{mount_dir}/{tmp_mount_args[1]}"
        tmp_mount_args[1] = target_mount_dir
        os.makedirs(tmp_mount_args[1])
        mount(*tmp_mount_args)


def bind_mount_to_host(mount_dir, path):
    target_path = Path(f"{mount_dir}{path}")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.touch()
    mount(path, target_path, None, MS_BIND | MS_REC)


def bind_working_dir(mount_dir):
    working_dir = os.getcwd()
    target_path = Path(mount_dir, working_dir[1:])
    target_path.mkdir(parents=True, exist_ok=True)
    mount(working_dir, target_path, None, MS_BIND | MS_REC)


class RootFS:
    def __init__(self, ram_disk_size: int) -> None:
        setup_user_level_root()
        root_mnt = create_root_tmpfs(ram_disk_size)
        bind_standard_mounts(root_mnt)

        for bind_path in ["/etc/group", "/etc/resolv.conf", "/etc/passwd"]:
            bind_mount_to_host(root_mnt, bind_path)

        if path_is_parent(os.path.expanduser("~"), os.getcwd()):
            bind_working_dir(root_mnt)
            start_dir = os.getcwd()
        else:
            start_dir = "/"
        self.root_mnt = root_mnt
        self.start_dir = start_dir

    def chroot(self):
        os.chroot(self.root_mnt)
        os.chdir(self.start_dir)

    def get_root(self):
        return self.root_mnt
