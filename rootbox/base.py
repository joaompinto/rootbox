import os

from .images import download_image
from .path import path_is_parent
from .rootfs import (
    bind_mount_to_host,
    bind_standard_mounts,
    bind_working_dir,
    create_root_tmpfs,
)
from .tar import extract_tar
from .unshare import setup_user_level_root


class BaseMounts:
    mount_list = []


def base_setup(image_name: str, ram_disk_size: int):
    """Setup the base rootfs and chroot into it"""

    setup_user_level_root()
    root_mnt = create_root_tmpfs(ram_disk_size)
    bind_standard_mounts(root_mnt)

    for bind_path in ["/etc/group", "/etc/resolv.conf", "/etc/passwd"]:
        bind_mount_to_host(root_mnt, bind_path)

    if ":" in image_name:
        image_fname = download_image(image_name)
    else:
        image_fname = image_name
    extract_tar(image_fname, root_mnt)

    if path_is_parent(os.path.expanduser("~"), os.getcwd()):
        bind_working_dir(root_mnt)
        start_dir = os.getcwd()
    else:
        start_dir = "/"

    os.chroot(root_mnt)
    os.chdir(start_dir)
    return root_mnt
