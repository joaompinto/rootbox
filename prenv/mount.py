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
