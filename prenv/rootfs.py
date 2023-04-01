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


def prepare_rootfs(rootfs_filename: str, until_tar: bool = False):
    set_user_level_root()
    mount(None, "/", None, MS_REC | MS_PRIVATE)
    mount_dir = Path(mkdtemp())
    mount("tmpfs", mount_dir, "tmpfs")
    extract_tar(rootfs_filename, mount_dir)
    root_content = [_ for _ in mount_dir.glob("*")]
    if len(root_content) == 1:
        mount_dir = mount_dir.joinpath(root_content[0])
    if until_tar:
        print("\nPaused after tar for debug")
        os.system("sh")
    os.chdir(mount_dir)
    for mount_args in STD_MOUNTS:
        os.makedirs(mount_args[1], exist_ok=True)
        mount(*mount_args)
    if Path(f"{mount_dir}/etc/resolv.conf").is_symlink():
        Path(f"{mount_dir}/etc/resolv.conf").unlink()
    with open(f"{mount_dir}/etc/resolv.conf", "w") as f:
        f.write("")
    mount("/etc/resolv.conf", f"{mount_dir}/etc/resolv.conf", None, MS_BIND)
