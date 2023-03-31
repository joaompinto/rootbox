import os
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


def prepare_rootfs(rootfs_filename: str):
    set_user_level_root()
    mount(None, "/", None, MS_REC | MS_PRIVATE)
    mount_dir = mkdtemp()
    mount("tmpfs", mount_dir, "tmpfs")
    os.chdir(mount_dir)
    for mount_args in STD_MOUNTS:
        os.makedirs(mount_args[1])
        mount(*mount_args)
    extract_tar(rootfs_filename, mount_dir)
    if os.path.exists(f"{mount_dir}/etc/resolv.conf"):
        os.unlink(f"{mount_dir}/etc/resolv.conf")
    with open(f"{mount_dir}/etc/resolv.conf", "w") as f:
        f.write("")
    mount("/etc/resolv.conf", f"{mount_dir}/etc/resolv.conf", None, MS_BIND),
