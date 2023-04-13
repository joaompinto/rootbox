import atexit
import os
import socket
import time
from pathlib import Path

import xdg

SOCKETS_DIR = Path(xdg.xdg_runtime_dir() or "/tmp", "rootbox")


def create_socket_bind():
    my_pid = os.getpid()
    SOCKETS_DIR.mkdir(parents=True, exist_ok=True)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    socket_path = Path(SOCKETS_DIR, f"rootbox.{my_pid}.sock")
    atexit.register(os.unlink, socket_path.as_posix())
    sock.bind(socket_path.as_posix())
    return sock


def get_process_socket(pid: int) -> socket.socket:
    socket_path = Path(SOCKETS_DIR, f"rootbox.{pid}.sock")

    # Wait for the child process to create the Unix socket
    while not socket_path.exists():
        time.sleep(0.01)

    conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    conn.connect(socket_path.as_posix())
    return conn
