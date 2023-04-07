import os
from pathlib import Path
from tempfile import mkdtemp

from .mount import MS_BIND, MS_PRIVATE, MS_REC, mount
from .tar import extract_tar
from .unshare import set_user_level_root

STD_MOUNTS = [
    ("/proc", "proc/", None, MS_BIND | MS_REC),
    ("/dev", "dev/", None, MS_BIND | MS_REC),
    ("/sys", "sys/", None, MS_BIND | MS_REC),
    ("tmpfs", "run/", "tmpfs"),
]


def prepare_rootfs(rootfs_filename: str, in_memory):
    set_user_level_root()
    mount(None, "/", None, MS_REC | MS_PRIVATE)
    mount_dir = Path(mkdtemp())
    if in_memory:
        mount("tmpfs", mount_dir, "tmpfs")
    extract_tar(rootfs_filename, mount_dir)
    os.chdir(mount_dir)
    for mount_args in STD_MOUNTS:
        os.makedirs(mount_args[1], exist_ok=True)
        mount(*mount_args)
    resolv_conf = Path(f"{mount_dir}/etc/resolv.conf")
    if resolv_conf.is_symlink():
        resolv_conf.unlink()
    if Path(mount_dir, "etc").exists():
        resolv_conf.touch()
        mount("/etc/resolv.conf", f"{mount_dir}/etc/resolv.conf", None, MS_BIND)
    return mount_dir
