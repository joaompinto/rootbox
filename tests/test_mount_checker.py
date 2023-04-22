from rootbox.cli.cmd_run import MountChecker


def test_mount_checker():
    MountChecker.read_mounts()
    assert MountChecker.is_on_mount_dir("/proc/1") is False
    assert MountChecker.is_on_mount_dir("/dev/abc") is False
    assert MountChecker.is_on_mount_dir("/local_file") is True
