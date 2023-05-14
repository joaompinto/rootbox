from rootbox.rootfs import RootFS


def test_rootfs():
    rootfs = RootFS(1)
    assert rootfs.get_root()
    rootfs.chroot()
