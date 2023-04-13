import os

from rootbox.mount import MS_BIND, MS_PRIVATE, MS_REC, mount
from rootbox.unshare import setup_user_level_root

setup_user_level_root()

# remount / as private to make subsequent mounts visible only to the current process and its descendants.
mount(None, "/", None, MS_REC | MS_PRIVATE)

os.chdir("/tmp/alpine")
mount("/proc", "proc/", None, MS_BIND | MS_REC)
mount("/dev", "dev/", None, MS_BIND | MS_REC)
mount("/sys", "sys/", None, MS_BIND | MS_REC)
mount("tmpfs", "run/", "tmpfs")

os.chroot(".")

# Spawn a shell
os.execv("/bin/sh", ["/bin/sh"])
