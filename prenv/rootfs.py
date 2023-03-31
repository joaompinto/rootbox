import os

from .mount import MS_BIND, MS_PRIVATE, MS_REC, mount
from .tar import extract_tar
from .unshare import set_user_level_root

STD_MOUNTS = [
    ("/proc", "proc/", None, MS_BIND | MS_REC),
    ("/dev", "dev/", None, MS_BIND | MS_REC),
    ("/sys", "sys/", None, MS_BIND | MS_REC),
    ("tmpfs", "run/", "tmpfs"),
]


def prepare_rootfs(rootfs_filename: str):
    set_user_level_root()
    mount(None, "/", None, MS_REC | MS_PRIVATE)
    mount("tmpfs", "/mnt", "tmpfs")
    os.chdir("/mnt")
    for mount_args in STD_MOUNTS:
        os.makedirs(mount_args[1])
        mount(*mount_args)
    extract_tar(rootfs_filename, "/mnt")
