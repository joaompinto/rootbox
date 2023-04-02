import ctypes
import os

from .socket import get_process_socket
from .unshare import CLONE_NEWNS, CLONE_NEWUSER

SYSCALL_PIDFD_OPEN = 434

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)


def enter_process(pid: int, no_shell, command) -> None:
    """Enter the process namespace of a given PID."""

    fd = libc.syscall(SYSCALL_PIDFD_OPEN, pid, 0, None, None, None)
    if fd < 0:
        print("pidfd_open failed: %s", ctypes.get_errno())
        return

    if libc.setns(fd, CLONE_NEWUSER | CLONE_NEWNS) < 0:
        errno = ctypes.get_errno()
        raise OSError(
            errno,
            f"setns failed: {os.strerror(errno)}",
        )

    conn = get_process_socket(pid)
    conn.sendall(b"info")
    data = conn.recv(1024)
    conn.close()
    os.chroot(data.decode("utf-8"))
    os.chdir("/")
    if no_shell:
        command = command.split()
        os.execvp(command[0], command[:])
    else:
        os.execvp("/bin/sh", ["sh", "-c", command])
