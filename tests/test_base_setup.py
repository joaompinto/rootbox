import os

from rootbox.base import base_setup


def test_base_setup():
    base_setup("lxc:busybox:1.34.1", 1)
    rc = os.system("ls -l /linuxrc")
    os.chroot("/host_root")
    assert rc == 0


if __name__ == "__main__":
    test_base_setup()
