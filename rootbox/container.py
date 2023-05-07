import os
from contextlib import contextmanager

from .enter import get_fd_for_process, set_namespace
from .process import create_manager_process
from .socket import get_process_socket


@contextmanager
def Container(image_name: str, ram_disk_size: int):
    cm = ContainerManager(image_name, ram_disk_size)
    try:
        yield cm
    finally:
        cm.stop()


class ContainerManager:
    def __init__(self, image_name, ram_disk_size) -> None:
        self.child_pid = None
        pid = create_manager_process(image_name, ram_disk_size)
        self.stop_pid = os.getpid()
        self.pid = pid
        conn = get_process_socket(pid)
        conn.sendall(b"info")
        data = conn.recv(1024)
        self.mount_point = data.decode("utf-8")
        conn.close()

    def stop(self):
        """only run stop if the process is the same as the one that started the manager"""
        if os.getpid() == self.stop_pid:
            try:
                conn = get_process_socket(self.pid)
                conn.sendall(b"terminate")
                conn.close()
            except ConnectionRefusedError:
                pass

    def run(self, command):
        conn = get_process_socket(self.pid)
        conn.sendall(b"info")
        data = conn.recv(1024).decode("utf-8")
        mount_point = data
        conn.close()
        pid = os.fork()
        if pid:
            pid, exit_code = os.wait()
            return exit_code
        else:
            self.child_pid = os.getpid()
            fd = get_fd_for_process(self.pid)
            set_namespace(fd)

            os.chroot(mount_point)
            os.chdir("/")
            rc = os.system(f"{command}")
            if rc != 0:
                raise RuntimeError(f"Command failed with exit code {rc}")
            # We do not want to raise SystemExit here, because we do not want
            # to run the atexit handlers in the child.
            os._exit(rc)
