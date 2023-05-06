import os

from rootbox.images import download_image
from rootbox.rootfs import bind_mount_to_host, bind_standard_mounts, create_root_tmpfs
from rootbox.tar import extract_tar
from rootbox.unshare import setup_user_level_root


def base_setup(image_name):
    """Setup the base rootfs and chroot into it"""
    setup_user_level_root()
    root_mnt = create_root_tmpfs()
    bind_standard_mounts(root_mnt)

    if ":" in image_name:
        image_fname = download_image(image_name)
    extract_tar(image_fname, root_mnt)
    for bind_path in ["/etc/group", "/etc/resolv.conf", "/etc/passwd"]:
        bind_mount_to_host(root_mnt, bind_path)

    os.chroot(root_mnt)
    os.chdir("/")
    return root_mnt
