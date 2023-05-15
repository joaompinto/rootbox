import os
import sys
from dataclasses import dataclass
from multiprocessing import Queue
from pathlib import Path

from .colorhelper import info
from .enter import set_namespace_pid
from .images import pull
from .images.tar import extract_tar
from .rootfs import RootFS
from .socket import create_socket_bind
from .verbose import verbose


def manager_process(queue: Queue, ram_disk_size: int) -> None:
    """The manager proccess performs the follwing maint tasks

    1. Creates a unix socket and waits to receive a connection and a "setup" message
    2. Once the message is received, it calls prepare_rootfs() function
    3. Once the rootfs is ready, it sends an "ok" message to the connection accepted on 1
    4. Keeps in a loop accepting connections and responding to "info" messages with the mount dir

    """
    verbose("Manager process started with pid", os.getpid())
    sock = create_socket_bind()
    sock.listen(1)

    rootfs = RootFS(ram_disk_size)
    root_mnt = rootfs.get_root()
    queue.put(root_mnt.as_posix())

    while True:
        conn, _ = sock.accept()
        message = conn.recv(1024).decode("utf-8")
        verbose("Received message from parent process: ", message)
        if message == "terminate":
            conn.close()
            break
        if message == "info":
            conn.sendall(root_mnt.as_posix().encode("utf-8"))
        else:
            print("Received unexpeted message from parent process: ", message)
        conn.close()


def setup_master_process(queue: Queue, pid: int, is_verbose=False) -> None:
    verbose("Waiting for mount point from the process manager")
    root_mnt = queue.get()
    verbose("mount point received", root_mnt)

    if is_verbose:
        if sys.stdout.isatty():
            print("Instance setup successfully with PID:", info(pid))
        else:
            print(pid)
    return root_mnt


@dataclass
class ProcessManager:
    ram_disk_size: int

    def __post_init__(self):
        verbose("ProcessManager: Creating process manager")
        queue = Queue()
        pid = os.fork()
        if pid == 0:
            manager_process(queue, self.ram_disk_size)
            exit(0)
        else:
            root_mnt = setup_master_process(queue, pid)
            self.root_mnt = root_mnt
            self.manager_pid = pid
            set_namespace_pid(pid)
        verbose("ProcessManager: end of ___post_init__")

    def get_pid(self) -> int:
        return self.manager_pid

    def get_root(self) -> Path:
        return Path(self.root_mnt)

    def apply_image(self, image_name) -> None:
        verbose(f"Applying image {image_name} from {os.getpid()}")
        if ":" in image_name:
            image_fname = pull(image_name)
        else:
            image_fname = image_name
        extract_tar(image_fname, self.root_mnt)
