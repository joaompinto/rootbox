import os

from rootbox.images import download_image
from rootbox.rootfs import bind_mount_to_host, prepare_root_mounts
from rootbox.tar import extract_tar
from rootbox.unshare import setup_user_level_root


def test_base_setup():
    setup_user_level_root()
    root_mnt = prepare_root_mounts()

    image_fname = download_image("lxc:busybox:1.34.1")
    extract_tar(image_fname, root_mnt)
    for bind_path in ["/etc/group", "/etc/resolv.conf", "/etc/passwd"]:
        bind_mount_to_host(root_mnt, bind_path)

    os.chroot(root_mnt)
    os.chdir("/")

    rc = os.system("ls -l /linuxrc")
    os.chroot("/host_root")
    assert rc == 0


if __name__ == "__main__":
    test_base_setup()
