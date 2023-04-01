import ctypes
import os
from pathlib import Path

CLONE_NEWNS = 0x20000
CLONE_NEWCGROUP = 0x2000000
CLONE_NEWUTS = 0x4000000
CLONE_NEWIPC = 0x8000000
CLONE_NEWUSER = 0x10000000
CLONE_NEWPID = 0x20000000
CLONE_NEWNET = 0x40000000
CLONE_NEWTIME = 0x80000000


libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)

libc.unshare.argtypes = (ctypes.c_int,)
libc.unshare.restype = ctypes.c_int


def unshare(flags: int):
    retry = 2  # Use retry to avoid "Invalid argument" randomly found on WSL2
    while True:
        ret = libc.unshare(flags)
        if ret == -1:
            errno = ctypes.get_errno()
            if errno == 22 and retry > 0:
                print("Retry unshare")
                retry -= 1
                continue
            else:
                raise OSError(
                    errno,
                    f"Fail to unshare with flags {flags:#x}: {os.strerror(errno)}",
                )
        break


def set_user_level_root():
    uid, gid = os.geteuid(), os.getegid()
    assert uid != 0 and gid != 0  # already have root privileges
    unshare(CLONE_NEWNS | CLONE_NEWUSER)
    Path("/proc/self/uid_map").write_text(f"0 {uid} 1")
    Path("/proc/self/setgroups").write_text("deny")
    Path("/proc/self/gid_map").write_text(f"0 {gid} 1")
