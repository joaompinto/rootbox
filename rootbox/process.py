import os

from .colorhelper import info, print_error
from .rootfs import prepare_rootfs
from .socket import create_socket_bind, get_process_socket
from .verbose import verbose


def child_process(tar_fname) -> None:
    sock = create_socket_bind()
    sock.listen(1)
    conn, _ = sock.accept()

    message = conn.recv(1024).decode("utf-8")
    if message != "setup":
        raise Exception(f"Unexpected message from parent process: {message}")
    verbose(f"Received message from parent process: {message}")
    mount_dir = prepare_rootfs(tar_fname, in_memory=True, perform_chroot=False)
    conn.sendall(b"ok")
    conn.close()

    while True:
        conn, _ = sock.accept()
        message = conn.recv(1024).decode("utf-8")
        if message == "info":
            conn.sendall(mount_dir.as_posix().encode("utf-8"))
        else:
            print("Received unexpeted message from parent process: ", message)
        conn.close()


def parent_process(pid: int) -> None:
    # Connect to the child process's Unix socket
    conn = get_process_socket(pid)
    conn.sendall(b"setup")

    # Wait for the setup result
    message = conn.recv(1024).decode("utf-8")
    if message == "ok":
        print("Instance setup successfully with PID:", info(pid))
    else:
        print_error(f"Failed to setup the instance: {message}")
        exit(2)


def create_child_process(tar_fname: str) -> None:
    """Create a master process that will create a new process namespace and
    mount a new root filesystem."""
    pid = os.fork()

    if pid == 0:
        child_process(tar_fname)
    else:
        parent_process(pid)
        return pid
