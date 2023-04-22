import os
from pathlib import Path
from tempfile import mkdtemp

from .mount import MS_BIND, MS_PRIVATE, MS_REC, mount
from .path import path_is_parent
from .tar import extract_tar
from .unshare import setup_user_level_root

STD_MOUNTS = [
    ("/", "host_root/", None, MS_BIND | MS_REC),
    ("/proc", "proc/", None, MS_BIND | MS_REC),
    ("/dev", "dev/", None, MS_BIND | MS_REC),
    ("/sys", "sys/", None, MS_BIND | MS_REC),
    ("tmpfs", "run/", "tmpfs"),
]


def prepare_rootfs(rootfs_filename: Path, ram_disk_size, perform_chroot=True) -> Path:
    """Preate a new root mount directory"""
    setup_user_level_root()
    current_path = os.getcwd()
    restore_path = None
    if path_is_parent(os.path.expanduser("~"), current_path):
        restore_path = current_path

    mount(None, "/", None, MS_REC | MS_PRIVATE)
    mount_dir = Path(mkdtemp())
    if ram_disk_size:
        mount("tmpfs", mount_dir, "tmpfs", options=f"size={ram_disk_size}G")
    if ".tar" in rootfs_filename.suffixes:
        extract_tar(rootfs_filename, mount_dir)
    else:
        raise NotImplementedError(f"Unsupported rootfs format: {rootfs_filename}")
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

    if perform_chroot:
        if restore_path:
            target_restore_path = Path(mount_dir, restore_path[1:])
            target_restore_path.mkdir(parents=True)
            mount(restore_path, target_restore_path, None, MS_BIND | MS_REC)
        else:
            target_restore_path = "/"
        os.chroot(mount_dir)
        os.chdir(restore_path or "/")
    return mount_dir
