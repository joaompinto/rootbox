import os
from pathlib import Path
from tempfile import mkdtemp

from .mount import bind_mount_to_host, bind_standard_mounts, bind_working_dir, mount
from .path import path_is_parent
from .unshare import setup_user_level_root


def create_root_tmpfs(ram_disk_size: int = 1):
    """Create a tmpfs file system and mount it on a random tmp directory"""
    if os.getuid() != 0:
        raise PermissionError("This function must be run with uid 0")
    mount_dir = Path(mkdtemp())
    mount("tmpfs", mount_dir, "tmpfs", options=f"size={ram_disk_size}G")
    return mount_dir


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
