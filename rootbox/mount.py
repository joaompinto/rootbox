import ctypes
import ctypes.util
import os
from pathlib import Path
from typing import Union

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
libc.mount.argtypes = (
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_ulong,
    ctypes.c_char_p,
)
libc.mount.restype = ctypes.c_int
libc.umount.argtypes = (ctypes.c_char_p,)
libc.umount.restype = ctypes.c_int

MS_RDONLY = 0x1
MS_NOSUID = 0x2
MS_NODEV = 0x4
MS_NOEXEC = 0x8
MS_SYNCHRONOUS = 0x10
MS_REMOUNT = 0x20
MS_MANDLOCK = 0x40
MS_DIRSYNC = 0x80
MS_NOATIME = 0x400
MS_NODIRATIME = 0x800
MS_BIND = 0x1000
MS_MOVE = 0x2000
MS_REC = 0x4000
MS_SILENT = 0x8000
MS_UNBINDABLE = 0x20000
MS_PRIVATE = 0x40000
MS_SLAVE = 0x80000
MS_SHARED = 0x100000
MS_RELATIME = 0x200000
MS_STRICTATIME = 0x1000000
MS_LAZYTIME = 0x2000000


def mount(
    device: Union[str, Path],
    mount_point: Union[str, Path],
    fs_type: str,
    flags: int = 0,
    options: str = "",
):
    ret = libc.mount(
        str(device).encode(),
        str(mount_point).encode(),
        fs_type.encode() if fs_type else None,
        flags,
        options.encode(),
    )
    if ret == -1:
        errno = ctypes.get_errno()
        raise OSError(
            errno,
            f'Fail to mount {device} ({fs_type}) on {mount_point} with "{options}": {os.strerror(errno)}',
        )


def umount(target: Union[str, Path]):
    ret = libc.umount(str(target).encode())
    if ret == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, f"Fail to umount {target}: {os.strerror(errno)}")


STD_MOUNTS = [
    ("/", "host_root/", None, MS_BIND | MS_REC),
    ("/proc", "proc/", None, MS_BIND | MS_REC),
    ("/dev", "dev/", None, MS_BIND | MS_REC),
    ("/sys", "sys/", None, MS_BIND | MS_REC),
    ("tmpfs", "run/", "tmpfs"),
]


def bind_standard_mounts(mount_dir):
    """Create the standards mounts on top of mount_dir"""

    if os.getuid() != 0:
        raise PermissionError("This function must be run with uid 0")

    for mount_args in STD_MOUNTS:
        tmp_mount_args = list(mount_args)
        target_mount_dir = f"{mount_dir}/{tmp_mount_args[1]}"
        tmp_mount_args[1] = target_mount_dir
        os.makedirs(tmp_mount_args[1])
        mount(*tmp_mount_args)


def bind_mount_to_host(mount_dir, path):
    target_path = Path(f"{mount_dir}{path}")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.touch()
    mount(path, target_path, None, MS_BIND | MS_REC)


def bind_working_dir(mount_dir):
    working_dir = os.getcwd()
    target_path = Path(mount_dir, working_dir[1:])
    target_path.mkdir(parents=True, exist_ok=True)
    mount(working_dir, target_path, None, MS_BIND | MS_REC)
